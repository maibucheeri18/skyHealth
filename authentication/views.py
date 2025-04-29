# Author: Student_D_Diego_Santos_de_Freitas 

import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse

from skyHealth.utils import get_user_level_context
from .forms import LoginForm, CreateAccountForm, SetSecurityQuestionsForm, CheckSecurityQuestionsForm, ResetPasswordForm
from database.models import UserProfile

def login_view(request):
    """
    Handle user authentication:
    - Authenticate via username or email
    - Redirect to dashboard on success
    - Show error on invalid credentials
    """

    context = get_user_level_context(request)
    print(context)
    user_level = context.get('user_level', 0)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # First try standard username authentication
            user = authenticate(request, username=username, password=password)

            # Fallback to email authentication if username fails
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            # This is has to be corrected based on the URL and user
            if user is not None:
                user_obj = UserProfile.objects.filter(user=user)

                print(user_level, user_obj)

                if user_level == 0 and user_obj[0].is_engineer:
                    auth_login(request, user)
                    return redirect('chooseSession')
                elif user_level == 1 and user_obj[0].is_team_leader:
                    auth_login(request, user)
                    return redirect('chooseSession')
                elif user_level == 2 and user_obj[0].is_department_leader:
                    auth_login(request, user)
                    return redirect('results')
                elif user_level == 3 and user_obj[0].is_senior_manager:
                    auth_login(request, user)
                    return redirect('results')
                else:
                    print("You idiot, use the correct area")
                
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

        print(form.errors)

        if form.is_valid():

            user = form.save()
            password = form.cleaned_data.get('password')

            user = authenticate(username=user.username, password=password)

            if user is not None:
                auth_login(request, user)
            print(password)
            return redirect('security_questions2')
        else:
            messages.error(request, "Error during authentication")
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
            try:
                profile = UserProfile.objects.get(user=user)
                profile.securityQuestion_Answer1 = form.cleaned_data['city']
                profile.securityQuestion_Answer2 = form.cleaned_data['company']
                profile.save()
                return redirect('login')
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(
                    user=user,
                    jobRole='Not specified',  # Default value
                    hireDate=datetime.now().date(),  # Default to today
                    securityQuestion_Answer1=form.cleaned_data['city'],
                    securityQuestion_Answer2=form.cleaned_data['company']
                )
    else:
        form = SetSecurityQuestionsForm()

    return render(request, 'securityquestions2.html', {'form': form})


def security_questions(request):
    """
    Verify identity via security questions for password recovery:
    - Check answers in UserProfile
    - Store verification in session if successful
    - Handle failed attempts with error messages
    """
    if request.method == 'POST':
        form = CheckSecurityQuestionsForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            company = form.cleaned_data['company']

            try:
                profile = UserProfile.objects.get(
                    securityQuestion_Answer1__iexact=city,
                    securityQuestion_Answer2__iexact=company
                )
                
                # Store verification in session
                request.session['reset_user_id'] = profile.user.id
                request.session.modified = True
                
                return redirect('reset_password')
            except UserProfile.DoesNotExist:
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
    if 'reset_user_id' not in request.session:
        messages.error(request, "Please answer security questions first.")
        return redirect('security_questions')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('reset_user_id')

            try:
                user = User.objects.get(id=user_id)
                user.set_password(form.cleaned_data['new_password'])
                user.save()

                # Clean up session
                request.session.pop('reset_user_id', None)
                
                messages.success(request, "Password has been reset successfully!")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'resetpassword.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def navbar(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            value = data.get('role')
            print(value)
            with open("./static/common.json", 'w') as f:
                json.dump({'role': value}, f)
    except:
        print("Error")




    return HttpResponse('Ok')

def dashboard(request):
    """Placeholder for future dashboard implementation"""
    return HttpResponse("Dashboard - Coming Soon")