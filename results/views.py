from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from skyHealth.utils import get_user_level_context
from database.models import Department, Team, HealthCheckCard, HealthCheckVote, User, UserProfile

import json
import matplotlib
import matplotlib.colors as mcolours
import matplotlib.pyplot as plt

import datetime

matplotlib.use('agg')

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
            engineer = UserProfile.objects.get(user_id=user_id, is_engineer=True)
            team = engineer.team
            context.update({
                'user_team': team,
                'available_teams': [team] if team else []
            })
        except UserProfile.DoesNotExist:
            context.update({'user_team': None, 'available_teams': []})

    elif user_level == 1:
        try:
            team_leader = UserProfile.objects.get(user_id=user_id, is_team_leader=True)
            led_team = team_leader.user.led_team
            department = led_team.department if led_team else None
            teams_in_department = Team.objects.filter(department=department) if department else []

            context.update ({
                'user_team': led_team,
                'available_teams': teams_in_department,
                'department': department
            })
        except UserProfile.DoesNotExist:
            context.update({'user_team': None, 'available_teams': [], 'department': None})

    elif user_level == 2:
        try: 
            dept_leader = UserProfile.objects.get(user_id=user_id, is_department_leader=True)
            led_department = dept_leader.user.led_department
            teams_in_department = Team.objects.filter(department=led_department) if led_department else []

            context.update({
                'user_department': led_department,
                'available_departments': Department.objects.all(),
                'available_teams': teams_in_department
            })
        except UserProfile.DoesNotExist:
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

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            votes = {}

            match(user_level):
                case 0:
                    user = UserProfile.objects.filter(user_id=request.user.id, is_engineer=True)
                case 1:
                    user = UserProfile.objects.filter(user_id=request.user.id, is_team_leader=True)
                case 2: 
                    user = UserProfile.objects.filter(user_id=request.user.id, is_department_leader=True)
                case 3: 
                    user = UserProfile.objects.filter(user_id=request.user.id, is_senior_manager=True)

            print(user)

            # engineer and their own team
            if data['type']:
                for t in data['type']:

                    if t == "Individual":
                        user_profile = UserProfile.objects.filter(user_id=request.user.id, is_engineer=True)

                        for c in data['healthCheckCard']:
                            card = HealthCheckCard.objects.filter(cardName = c)

                            checkVotes = HealthCheckVote.objects.filter(user = user_profile[0].user, card = card[0])

                            red = 0
                            amber = 0 
                            green = 0

                            for v in checkVotes:
                                if len(data['progressOverTime']) != 0:
                                    oldDate = datetime.datetime(
                                        v.dateCompleted.year,
                                        v.dateCompleted.month+int(data['progressOverTime'][0]),
                                        v.dateCompleted.day
                                    )

                                    if oldDate < datetime.datetime.now():
                                        continue

                                match(v.vote.voteColour.lower()):
                                    case 'red':
                                        red += 1
                                    case 'green':
                                        green += 1
                                    case 'amber':
                                        amber += 1
                    
                            votes.update({card[0].cardName: [red, amber, green]})

                    else:
                        team = Team.objects.filter(teamName = t)

                        if len(team) == 0:
                            continue

                        for c in data['healthCheckCard']:
                            card = HealthCheckCard.objects.filter(cardName = c)

                            checkVotes = HealthCheckVote.objects.filter(team = team[0], card = card[0])

                            red = 0
                            amber = 0 
                            green = 0

                            for v in checkVotes:
                                if len(data['progressOverTime']) != 0:
                                    oldDate = datetime.datetime(
                                        v.dateCompleted.year,
                                        v.dateCompleted.month+int(data['progressOverTime'][0]),
                                        v.dateCompleted.day
                                    )

                                    if oldDate < datetime.datetime.now():
                                        continue

                                match(v.vote.voteColour.lower()):
                                    case 'red':
                                        red += 1
                                    case 'green':
                                        green += 1
                                    case 'amber':
                                        amber += 1

                        votes.update({card[0].cardName: [red, amber, green]})
            
            # team leader and department leader 
            if data['team']:
                for t in data['team']:
                    team = Team.objects.filter(teamName = t)

                    for c in data['healthCheckCard']:
                        card = HealthCheckCard.objects.filter(cardName = c)
                        checkVotes = HealthCheckVote.objects.filter(team = team[0], department=team[0].department, card = card[0])

                        red = 0
                        amber = 0
                        green = 0

                        for v in checkVotes:
                            if len(data['progressOverTime']) != 0:
                                oldDate = datetime.datetime(
                                    v.dateCompleted.year,
                                    v.dateCompleted.month+int(data['progressOverTime'][0]),
                                    v.dateCompleted.day
                                )

                                if oldDate < datetime.datetime.now():
                                    continue
                            
                            match (v.vote.voteColour.lower()):
                                case 'red':
                                    red += 1
                                case 'green':
                                    green += 1
                                case 'amber':
                                    amber += 1

                        votes.update({card[0].cardName: [red, amber, green]})

            # senior manager
            if data['department']:
                for d in data['department']:
                    dep = Department.objects.filter(departmentName = d)

                    for c in data['healthCheckCard']:
                        card = HealthCheckCard.objects.filter(cardName =c )
                        checkVotes = HealthCheckVote.objects.filter(department = dep[0], card = card[0])

                        red = 0 
                        amber = 0
                        green = 0

                        for v in checkVotes:
                            if len(data['progressOverTime']) != 0:
                                oldDate = datetime.datetime(
                                    v.dateCompleted.year,
                                    v.dateCompleted.month+int(data['progressOverTime'][0]),
                                    v.dateCompleted.day
                                )

                                if oldDate < datetime.datetime.now():
                                    continue
                        
                            match (v.vote.voteColour.lower()):
                                case 'red':
                                    red += 1
                                case 'green':
                                    green += 1
                                case 'amber':
                                    amber += 1

                        votes.update({card[0].cardName: [red, amber, green]})
            print(votes)

            filename = __make_graph(votes)

            response = {}

            response['message'] = "Working"

            return JsonResponse({'img':filename})

        except json.JSONDecodeError:
            print("Failed to load json")

    return render(request, 'results.html', context)

def __make_graph(v):
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Roboto']

    for key, value in v.items():
        plt.bar(key, value[0], color='#DD1717')
        plt.bar(key, value[1], bottom=value[0], color='#F15A22')
        plt.bar(key, value[2], bottom=value[0]+value[1], color='#007e13')

    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10)
    plt.tight_layout()

    date = datetime.datetime.now().hour + datetime.datetime.now().minute+datetime.datetime.now().microsecond
    filename = "fig-"+str(date)+".png"

    plt.savefig('.//static//img//' + filename)

    return filename