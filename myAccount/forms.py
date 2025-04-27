# forms.py
from django import forms
from django.contrib.auth.password_validation import validate_password
from database.models import Engineer, TeamLeader, DepartmentLeader, SeniorManager

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        # We'll use fields common to all user types
        fields = ['fName', 'lName', 'email', 'username', 'password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rename fields to match your HTML template
        self.fields['fName'].label = 'First name'
        self.fields['lName'].label = 'Last name'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Check if username changed and if new username already exists
        if username != self.instance.username:
            # Check across all user types
            if (Engineer.objects.filter(username=username).exists() or
                TeamLeader.objects.filter(username=username).exists() or
                DepartmentLeader.objects.filter(username=username).exists() or
                SeniorManager.objects.filter(username=username).exists()):
                raise forms.ValidationError("The username has already been taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required")
        
        # Check if email changed and if new email already exists
        if email != self.instance.email:
            if (Engineer.objects.filter(email=email).exists() or
                TeamLeader.objects.filter(email=email).exists() or
                DepartmentLeader.objects.filter(email=email).exists() or
                SeniorManager.objects.filter(email=email).exists()):
                raise forms.ValidationError("This email is already in use.")
        return email
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password, self.instance)
        return password

# Create specific forms for each user type if needed
class EngineerProfileForm(UserProfileForm):
    class Meta(UserProfileForm.Meta):
        model = Engineer

class TeamLeaderProfileForm(UserProfileForm):
    class Meta(UserProfileForm.Meta):
        model = TeamLeader

class DepartmentLeaderProfileForm(UserProfileForm):
    class Meta(UserProfileForm.Meta):
        model = DepartmentLeader

class SeniorManagerProfileForm(UserProfileForm):
    class Meta(UserProfileForm.Meta):
        model = SeniorManager