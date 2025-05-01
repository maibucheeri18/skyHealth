# Author: Student_B_Aathika_Ajmal_Basha

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from database.models import User

from .forms import AccountForm
import json

@login_required
def account_view(request):
    # Get the current user
    user = request.user
    user = User.objects.filter(id=user.id)[0]
    
    # For GET requests (read-only mode)
    if request.method == 'GET':

        return render(request, 'account.html', {'user': user})
    
    # For POST requests (form submission)
    elif request.method == 'POST':
        
        try:

            data = json.loads(request.body)
            print(data)
            # Get form data
            fName = data['first_name']
            lName = data['last_name']
            email = data['email']
            username = data['username']
            password = data['password']
            
            # Update user information
            user.first_name = fName
            user.last_name = lName
            user.email = email
            user.username = username
            
            # Update password if provided and not placeholder
            if password and password != '••••••••••••':
                user.set_password(password)
            

            # Save changes
            user.save()

            print(User.objects.filter(id=user.id)[0].first_name)

        except:
            print('JSON ERROR')
            
        return redirect('/account/')  # Make sure this matches your URL name
    return(request, 'account.html')
   