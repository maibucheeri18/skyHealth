from django import forms
from database.models import Vote, Session, HealthCheckVote, HealthCheckCard
from datetime import date

# form for creating Vote entries from the health check form
class VoteForm(forms.ModelForm):

    #options for color and progress fields
    colorOptions = [
        ('', 'Select color'),
        ('green', 'Green'),
        ('amber', 'Amber'),
        ('red', 'Red'),
    ]

    progressOptions = [
        ('', 'Select progress'),
        ('stable', 'Stable'),
        ('improving', 'Improving'),
        ('worse', 'Getting worse'),
    ]

    #fields for color selection
    voteColour = forms.ChoiceField(
        choices = colorOptions,
        required = True,
        widget = forms.Select(attrs={'id': 'color'})
    )

    #fields for progress indicator
    progressIndicator = forms.ChoiceField(
        choices = progressOptions,
        required = True,
        widget = forms.Select(attrs={'id': 'progress'})
    )

    #field for user comment
    voteComment = forms.CharField(
        required = True,
        widget = forms.Textarea(attrs={
            'id': 'comment',
            'placeholder': 'Add your comment'
        })
    )

    class Meta:
        model = Vote
        fields = ['voteColour', 'progressIndicator', 'voteComment']

    # extract session from kwargs
    #overrides __init__ to accept the session
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super(VoteForm, self).__init__(*args, **kwargs)
        
    # saves the vote and links it with the session
    def save(self, commit=True):
        vote = super(VoteForm, self).save(commit=False)
        
        if self.session:
            vote.session = self.session
            
        if commit:
            vote.save()
        
        return vote

# creates a relationship between vote and a specific healthCheck card
class HealthCheckVoteForm(forms.Form):

    # hidden field to pass the healthCheckCard ID
    card_id = forms.IntegerField(widget=forms.HiddenInput())

    #overrides __init__ to accept session and card
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        self.card = kwargs.pop('card', None)
        super(HealthCheckVoteForm, self).__init__(*args, **kwargs)

        #embeds the VoteForm inside the form
        self.vote_form = VoteForm(*args, **kwargs, session=self.session)

        if self.card:
            self.fields['card_id'].initial = self.card.cardId

    #validation to check that the card form and the embedded vote form must be valid
    def is_valid(self):
        return super(HealthCheckVoteForm, self).is_valid() and self.vote_form.is_valid()

    #save method that creates both a Vote and HealthCheckVote
    def save(self, commit=True):
        vote = self.vote_form.save(commit=commit)

        if commit:
            try:
                card_id = self.cleaned_data['card_id']
                card = HealthCheckCard.objects.get(cardId=card_id)

                health_check_vote = HealthCheckVote(
                    vote = vote,
                    card = card,
                    dateCompleted = date.today()
                )
                health_check_vote.save()

                return health_check_vote
            
            except HealthCheckCard.DoesNotExist:
                if vote and hasattr(vote, 'id'):
                    vote.delete()
                raise ValueError("Health check card was not found")