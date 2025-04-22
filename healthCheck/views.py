from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def startPage(request):
    return render(request, 'startPage.html')