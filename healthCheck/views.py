from django.shortcuts import render
from django.http import HttpResponse
from database.models import Session
from database.models import Team

# Create your views here.
def chooseSession(request):
    sessions = Session.objects.all()   #retrieving all session objects
    return render(request, 'chooseSession.html', {'sessions': sessions})

def chooseTeam(request):
    teams = Team.objects.all()
    return render(request, 'chooseTeam.html', {'teams': teams})

def startPage(request):
    return render(request, 'startPage.html')

def healthCheckForm(request):
    return render(request, 'healthCheckForm.html')

def closingPage(request):
    return render(request, 'closingPage.html')