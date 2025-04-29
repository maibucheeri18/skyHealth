from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# this is based on the SQL Query that was created in coursework one
    
class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=50, unique=True)
    numOfTeam = models.IntegerField()
    deptCreateDate = models.DateField()
    departmentLocation = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='led_department')

    def __str__(self):
        return self.departmentName
    
    class Meta: 
        db_table = 'Department'

class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=20, unique=True)
    numOfMembers = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teams')
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='led_team')

    def __str__(self):
        return self.teamName
    
    class Meta:
        db_table = 'Team'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    hireDate = models.DateField()
    securityQuestion_Answer1 = models.CharField(max_length=100)
    securityQuestion_Answer2 = models.CharField(max_length=100)

    is_engineer = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)
    is_department_leader = models.BooleanField(default=False)
    is_senior_manager = models.BooleanField(default=False)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='engineers')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        db_table = 'UserProfile'

class HealthCheckCard(models.Model):
    cardId = models.AutoField(primary_key=True)
    cardName = models.CharField(max_length=50)
    redColorDescrip = models.CharField(max_length=255) # THIS MIGHT CHANGE BECAUSE A 100 IS TOO LIMITED FOR DESCRIP
    greenColorDescrip = models.CharField(max_length=255)

    class Meta:
        db_table = 'HealthCheck_Card' 

class Session(models.Model):
    sessionId = models.AutoField(primary_key=True)
    sessionDate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'Session' 

class Vote(models.Model):
    voteId = models.AutoField(primary_key=True)
    voteColour = models.CharField(max_length=10)
    progressIndicator = models.CharField(max_length=20)
    voteComment = models.CharField(max_length=500)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Vote' 

class HealthCheckVote(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    card = models.ForeignKey(HealthCheckCard, on_delete=models.CASCADE)
    dateCompleted = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'HealthCheck_Vote' 
        unique_together = (('vote', 'card', 'dateCompleted'),)