from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return render(request, 'login.html')

def security_questions(request):
    return render(request, 'securityquestions.html')

def reset_password(request):
    return render(request, 'resetpassword.html')

def create_account(request):
    return render(request, 'createaccount.html')

def security_questions2(request):
    return render(request, 'securityquestions2.html')