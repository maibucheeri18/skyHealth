# Author: Student_B_Aathika_Ajmal_Basha

from django import forms
from django.contrib.auth.models import User
import re

class AccountForm(forms.ModelForm):
    # Override the fields to customize the form
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': ''})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': ''})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': ''})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError 
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError
        if len(password) < 8:
            raise forms.ValidationError
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError
        if not re.search(r'[\W_]', password):
            raise forms.ValidationError
        return password