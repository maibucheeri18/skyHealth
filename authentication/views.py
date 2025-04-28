# Author: Student_D_Diego_Santos_de_Freitas 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import LoginForm, CreateAccountForm, SetSecurityQuestionsForm, CheckSecurityQuestionsForm, ResetPasswordForm
from database.models import User, Engineer, TeamLeader, DepartmentLeader, SeniorManager

def login_view(request):
    """
    Handle user authentication:
    - Authenticate via username or email
    - Redirect to dashboard on success
    - Show error on invalid credentials
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # First try standard username authentication
            user = authenticate(request, username=username, password=password)

            # Fallback to email authentication if username fails
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
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username/email or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def create_account(request):
    """
    Handle new user registration:
    - Save user details
    - Auto-login after registration
    - Redirect to security questions setup
    """
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
    """
    Set security questions for new accounts:
    - Store answers in user profile
    - Redirect to login after completion
    """
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
    """
    Verify identity via security questions for password recovery:
    - Check answers across all user types
    - Store verification in session if successful
    - Handle failed attempts with error messages
    """
    if request.method == 'POST':
        form = CheckSecurityQuestionsForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            company = form.cleaned_data['company']

            user_classes = [Engineer, TeamLeader, DepartmentLeader, SeniorManager]
            found_user = False
            
            for model in user_classes:
                try:
                    user = model.objects.get(
                        securityQuestion_Answer1__iexact=city,
                        securityQuestion_Answer2__iexact=company
                    )
                    
                    # Store verification in session
                    request.session['reset_user_id'] = user.id
                    request.session['reset_user_model'] = model.__name__
                    request.session.modified = True
                    
                    found_user = True
                    return redirect('reset_password')

                except model.DoesNotExist:
                    continue
            
            if not found_user:
                messages.error(request, "Security answers didn't match any user.")
        else:
            messages.error(request, "Please fill in all fields correctly.")
    else:
        form = CheckSecurityQuestionsForm()

    return render(request, 'securityQuestions.html', {'form': form})


def reset_password(request):
    """
    Handle password reset after security verification:
    - Verify session contains valid reset request
    - Update password for identified user
    - Clear session data after completion
    """
    # Verify proper verification flow
    if 'reset_user_id' not in request.session or 'reset_user_model' not in request.session:
        messages.error(request, "Please answer security questions first.")
        return redirect('security_questions')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')
            user_model_name = request.session.get('reset_user_model')

            # Map model names to actual classes
            model_map = {
                'Engineer': Engineer,
                'TeamLeader': TeamLeader,
                'DepartmentLeader': DepartmentLeader,
                'SeniorManager': SeniorManager
            }
            model = model_map.get(user_model_name)

            if model:
                try:
                    user = model.objects.get(id=user_id)
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()

                    # Clean up session
                    request.session.pop('reset_user_id', None)
                    request.session.pop('reset_user_model', None)
                    
                    messages.success(request, "Password has been reset successfully!")
                    return redirect('login')
                except model.DoesNotExist:
                    messages.error(request, "Something went wrong. Please try again.")
                    return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'resetpassword.html', {'form': form})


def dashboard(request):
    """Placeholder for future dashboard implementation"""
    return HttpResponse("Dashboard - Coming Soon")