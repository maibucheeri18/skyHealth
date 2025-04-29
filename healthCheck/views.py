from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from database.models import Session
from database.models import Team
from database.models import HealthCheckCard
from .forms import HealthCheckVoteForm

# Create your views here.

#View for selecting a session
@login_required
def chooseSession(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        
        if session_id:
            #saving sessionId into user's session storage
            request.session['session_id'] = session_id
            return redirect('chooseTeam')

    sessions = Session.objects.all()   #retrieving all session objects
    return render(request, 'chooseSession.html', {'sessions': sessions})

#View for selecting a team
@login_required
def chooseTeam(request):
    teams = Team.objects.all()
    return render(request, 'chooseTeam.html', {'teams': teams})

#View for healthCheck startPage
@login_required
def startPage(request):
    return render(request, 'startPage.html')

# view for the healthCheckForm
@login_required
def healthCheckForm(request, card_index=0):
    # retrieve the 10 health check cards
    cards = HealthCheckCard.objects.all()[:10]

    #check that the card_index is within range
    if card_index < 0:
        card_index = 0 
    if card_index >= len(cards):
        card_index = len(cards) -1

    current_card = cards[card_index]

    # calculate progress bar percentage
    progress_percentage = (card_index * 100) // len(cards) 

    #get current sesssionId
    current_session = None
    if request.session.get('session_id'):
        try:
            current_session = Session.objects.get(sessionId=request.session.get('session_id'))
        except Session.DoesNotExist:
            #if session not found user will be redirected to chooseSession
            return redirect('chooseSession')
    else:
        return redirect('chooseSession')
    
    if request.method == 'POST':
        # process form submission
        form = HealthCheckVoteForm(request.POST, session=current_session, card=current_card)
        
        if form.is_valid():
            # saves vote & health check vote
            form.save()
            
            # determine where to redirect based on card index
            if card_index >= len(cards) - 1:
                return redirect('closingPage')
            else:
                return redirect('healthCheckForm', card_index=card_index + 1)
    else:
        # display empty form
        form = HealthCheckVoteForm(session=current_session, card=current_card)

    return render(request, 'healthCheckForm.html', {
        'card': current_card,
        'card_index': card_index,
        'total_cards': len(cards),
        'progress_percentage': progress_percentage,
        'form': form,
    })

#View for the closingPage
@login_required
def closingPage(request):
    return render(request, 'closingPage.html')