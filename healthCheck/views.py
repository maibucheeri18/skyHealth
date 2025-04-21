from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def votingForm(request):
    return render(request, 'votingForm.html')