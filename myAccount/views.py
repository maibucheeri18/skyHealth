# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from database.models import Engineer, TeamLeader, DepartmentLeader, SeniorManager

#login_required
def account_view(request):
    # Get the current user
    user = request.user
    
    # For GET requests (read-only mode)
    if request.method == 'GET':
        return render(request, 'account.html', {'user': user})
    
    # For POST requests (form submission)
    elif request.method == 'POST':
        # Get form data
        fName = request.POST.get('first_name')
        lName = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validation (server-side)
        errors = {}
        
        # Username validation
        if not username:
            errors['username'] = 'Username is required'
        elif username != user.username:
            # Check across all user types
            if (Engineer.objects.filter(username=username).exists() or
                TeamLeader.objects.filter(username=username).exists() or
                DepartmentLeader.objects.filter(username=username).exists() or
                SeniorManager.objects.filter(username=username).exists()):
                errors['username'] = 'The username has already been taken'
        
        # Email validation
        if not email:
            errors['email'] = 'Email is required'
        elif email != user.email:
            # Check across all user types
            if (Engineer.objects.filter(email=email).exists() or
                TeamLeader.objects.filter(email=email).exists() or
                DepartmentLeader.objects.filter(email=email).exists() or
                SeniorManager.objects.filter(email=email).exists()):
                errors['email'] = 'This email is already in use'
        
        # If there are errors, return them
        if errors:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
            # For non-AJAX requests, return errors with the template
            return render(request, 'account.html', {
                'user': user,
                'errors': errors
            })
        
        # Update user information
        user.fName = fName
        user.lName = lName
        user.email = email
        user.username = username
        
        # Update password if provided and not placeholder
        if password and password != '••••••••••••':
            user.set_password(password)
        
        # Save changes
        user.save()
        
        # Return response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('account')  # Make sure this matches your URL name
    return(request, 'account.html')
    