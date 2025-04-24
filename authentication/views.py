from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .forms import LoginForm, CreateAccountForm

# Create your views here.

def login(request):
    """Handle user login"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username
            user = authenticate(request, username=username, password=password)
            
            # If username authentication fails, try with email
            if user is None:
                try:
                    # Look up user by email
                    from django.contrib.auth.models import User
                    user_obj = User.objects.get(email=username)
                    # Try to authenticate with the found username
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                auth_login(request, user)
                # Redirect to dashboard or home page after login
                return redirect('dashboard')  # Replace with your target URL name
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
            # Save the user
            user = form.save()
            
            # Log the user in automatically
            auth_login(request, user)
            
            # Redirect to the create security questions page
            return redirect('security_questions2')
    else:
        form = CreateAccountForm()
    
    return render(request, 'createaccount.html', {'form': form})

def security_questions(request):
    return render(request, 'securityquestions.html')

def reset_password(request):
    return render(request, 'resetpassword.html')

def security_questions2(request):
    return render(request, 'securityquestions2.html')