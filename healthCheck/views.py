from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def chooseSession(request):
    return render(request, 'chooseSession.html')

def chooseTeam(request):
    return render(request, 'chooseTeam.html')

def startPage(request):
    return render(request, 'startPage.html')

def healthcheckForm(request):
    return render(request, 'healthcheckForm.html')

def closingPage(request):
    return render(request, 'closingPage.html')