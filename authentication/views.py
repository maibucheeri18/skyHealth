from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import LoginForm, CreateAccountForm, SetSecurityQuestionsForm, CheckSecurityQuestionsForm, ResetPasswordForm
from database.models import Engineer, TeamLeader, DepartmentLeader, SeniorManager

def login_view(request):
    """Handle user login or redirect to forgotten password"""
    if request.method == 'POST':
        if 'forgot_password' in request.POST:
            return redirect('security_questions')

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)

            # Try authenticating with email
            if user is None:
                user_classes = [Engineer, TeamLeader, DepartmentLeader, SeniorManager]
                for model in user_classes:
                    try:
                        user_obj = model.objects.get(email=username)
                        user = authenticate(request, username=user_obj.username, password=password)
                        break
                    except model.DoesNotExist:
                        continue
            
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # Or your home/dashboard page
            else:
                messages.error(request, 'Invalid username/email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def create_account(request):
    """Handle new account creation"""
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('security_questions2')
    else:
        form = CreateAccountForm()
    return render(request, 'createaccount.html', {'form': form})


def security_questions2(request):
    """Collect security questions after account creation"""
    if request.method == 'POST':
        form = SetSecurityQuestionsForm(request.POST)
        if form.is_valid():
            user = request.user
            user.securityQuestion_Answer1 = form.cleaned_data['city']
            user.securityQuestion_Answer2 = form.cleaned_data['company']
            user.save()
            return redirect('login')
    else:
        form = SetSecurityQuestionsForm()

    return render(request, 'securityquestions2.html', {'form': form})



def security_questions(request):
    """Verify user's identity with security questions (forgotten password)"""
    if request.method == 'POST':
        form = CheckSecurityQuestionsForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            company = form.cleaned_data['company']

            user_classes = [Engineer, TeamLeader, DepartmentLeader, SeniorManager]
            for model in user_classes:
                try:
                    # Check if the answers match the security questions of the user
                    user = model.objects.get(
                        securityQuestion_Answer1__iexact=city,
                        securityQuestion_Answer2__iexact=company
                    )
                    # Store the user ID and model type in the session for later use
                    request.session['reset_user_id'] = user.id
                    request.session['reset_user_model'] = model.__name__

                    # Redirect to the reset_password view
                    return redirect('reset_password')

                except model.DoesNotExist:
                    continue

            # If no match was found, show an error
            messages.error(request, "Security answers didn't match any user.")
    else:
        form = CheckSecurityQuestionsForm()

    return render(request, 'resetpassword.html', {'form': form})


def reset_password(request):
    """Reset password after verifying security questions"""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # Get the user ID and model name from session
            user_id = request.session.get('reset_user_id')
            user_model_name = request.session.get('reset_user_model')

            # Map model name to the actual model class
            model_map = {
                'Engineer': Engineer,
                'TeamLeader': TeamLeader,
                'DepartmentLeader': DepartmentLeader,
                'SeniorManager': SeniorManager
            }
            model = model_map.get(user_model_name)

            if model:
                try:
                    # Get the user object based on the ID stored in the session
                    user = model.objects.get(id=user_id)

                    # Set the new password
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()

                    # Clear the session data after password reset
                    request.session.flush()

                    # Redirect to the login page after resetting the password
                    return redirect('login')
                except model.DoesNotExist:
                    messages.error(request, "Something went wrong. Please try again.")
    else:
        form = ResetPasswordForm()

    return render(request, 'login.html', {'form': form})


def dashboard(request):
        """Handle dashboard view"""
        return HttpResponse("Dashboard - Coming Soon")
