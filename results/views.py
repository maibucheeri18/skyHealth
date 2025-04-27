from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from skyHealth.utils import get_user_level_context
from database.models import Department, Team, HealthCheckCard, Engineer, TeamLeader, DepartmentLeader, SeniorManager

# Create your views here.
# results page
@login_required
def results(request):
    # the following is regarding adapting the search filter based on the user logged in
    context = get_user_level_context(request)
    user_level = context.get('user_level', 0)

    health_check_cards = HealthCheckCard.objects.all()
    user_id = request.user.id 

    if user_level == 0:
        try: 
            engineer = Engineer.objects.get(id=user_id)
            team = engineer.team
            context.update({
                'user_team': team,
                'available_teams': [team] if team else []
            })
        except Engineer.DoesNotExist:
            context.update({'user_team': None, 'available_teams': []})

    elif user_level == 1:
        try:
            team_leader = TeamLeader.objects.get(id=user_id)
            led_team = team_leader.led_team
            department = led_team.department if led_team else None
            teams_in_department = Team.objects.filter(department=department) if department else []

            context.update ({
                'user_team': led_team,
                'available_teams': teams_in_department,
                'department': department
            })
        except TeamLeader.DoesNotExist:
            context.update({'user_team': None, 'available_teams': [], 'department': None})

    elif user_level == 2:
        try: 
            dept_leader = DepartmentLeader.objects.get(id=user_id)
            led_department = dept_leader.led_department
            teams_in_department = Team.objects.filter(department=led_department) if led_department else []

            context.update({
                'user_department': led_department,
                'available_departments': Department.objects.all(),
                'available_teams': teams_in_department
            })
        except DepartmentLeader.DoesNotExist:
            context.update({
                'user_department': None,
                'available_departments': [],
                'available_teams': []
            })

    elif user_level == 3:
        all_departments = Department.objects.all()
        all_teams = Team.objects.all()

        context.update({
            'available_departments': all_departments,
            'available_teams': all_teams
        })

    context.update({
        'show_engineer_filters': user_level == 0,
        'show_team_leader_filters': user_level == 1,
        'show_department_leader_filters': user_level == 2,
        'show_senior_manager_filters': user_level == 3,
        'health_check_cards': health_check_cards
    })


    # retrieving the objects to be implemented in the dropdowns
    departments = Department.objects.values('departmentName')
    teams = Team.objects.values('teamName')
    healthCheckCards = HealthCheckCard.objects.values('cardName')

    return render(request, 'results.html', context)