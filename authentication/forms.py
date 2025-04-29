# Author: Student_D_Diego_Santos_de_Freitas 

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from database.models import UserProfile, Team, Department

import datetime

# Form for user login with username/email and password fields
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username or email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

# Form for creating a new user account with personal information
class CreateAccountForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create your password'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
    
    # Override save method to properly handle password hashing and create UserProfile
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create corresponding UserProfile
            u = UserProfile(
                user=user,
                hireDate=datetime.datetime.now(),
                securityQuestion_Answer1='',  # Will be filled out in security questions form
                securityQuestion_Answer2='',  # Will be filled out in security questions form
            )
            u.save()
        return user

# Form for setting security questions during account creation/recovery
class SetSecurityQuestionsForm(forms.Form):
    city = forms.CharField(
        label="What is the name of the city you were born in?",
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    company = forms.CharField(
        label="What is the name of the first company you worked for?",
        widget=forms.TextInput(attrs={'placeholder': 'First job company'})
    )

# Form for verifying security questions during password recovery
class CheckSecurityQuestionsForm(forms.Form):
    city = forms.CharField(
        label="What is the name of the city you were born in?",
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    company = forms.CharField(
        label="What is the name of the first company you worked for?",
        widget=forms.TextInput(attrs={'placeholder': 'First job company'})
    )

# Form for resetting password with validation to ensure passwords match
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label="Enter new password",
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'})
    )
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )
    
    # Custom validation to check if passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data