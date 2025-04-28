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
    
    try: 
        profile = request.user.profile

        user_level = 0
        user_role = 'Engineer'

        if profile.is_senior_manager:
            user_level = 3
            user_role = 'Senior Manager'
        elif profile.is_department_leader:
            user_level = 2
            user_role = 'Department Leader'
        elif profile.is_team_leader:
            user_level = 1
            user_role = 'Team Leader'

        has_heath_check_access = profile.is_engineer or profile.is_team_leader
    except AttributeError:
        user_level = 0
        user_role = 'Engineer'
        has_heath_check_access = True

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
        return redirect('login') 
    
    try:
        user_level = request.user.profile.level
    except AttributeError:
        user_level = 0

    if user_level in [0, 1]:
        return redirect(reverse('chooseSession')) 
    
    else: 
        return redirect(reverse('results')) 
    