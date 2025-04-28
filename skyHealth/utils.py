from django.shortcuts import redirect
from django.urls import reverse

# returns context data for the navbar based on the user's role level
def get_user_level_context(request):
    if not request.user.is_authenticated: 
        return {
            'is_logged_in': False,
            'user_level': None,
            'user_role': None
        }
    
    # this should be improved and updated on the database
    try: 
        user_level = request.user.profile.level
    except AttributeError:
        user_level = 0

    role_mapping = {
        0: 'Engineer',
        1: 'Team Leader',
        2: 'Department Leader',
        3: 'Senior Manager'
    }

    user_role = role_mapping.get(user_level, 'Engineer')

    has_heath_check_access = user_level in [0, 1]

    context = {
        'is_logged_in': True,
        'user_level': user_level,
        'user_role': user_role,
        'has_health_check_access': has_heath_check_access
    }

    return context

# determines where to redirect users after login based on the user role
def handle_login_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login') # this will change based on the pages
    
    try:
        user_level = request.user.profile.level
    except AttributeError:
        user_level = 0

    if user_level in [0, 1]:
        return redirect(reverse('health_check:choose_session')) # this will change based on the pages
    
    else: 
        return redirect(reverse('results:dashboard')) # this will change based on the pages
    