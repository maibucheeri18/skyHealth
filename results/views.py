from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from skyHealth.utils import get_user_level_context

# Create your views here.
# results page
@login_required
def results(request):
    # the following is regarding adapting the search filter based on the user logged in
    context = get_user_level_context(request)

    user_level = context.get('user_level', 0)

    context.update({
        'show_engineer_filters': user_level == 0,
        'show_team_leader_filters': user_level == 1,
        'show_department_leader_filters': user_level == 2,
        'show_senior_manager_filters': user_level == 3,
    })

    return render(request, 'results.html', context)