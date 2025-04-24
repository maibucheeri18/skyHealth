from django.db import models
# Django's built-in User model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# this is based on the SQL Query that was created in coursework one

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email: 
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username, 
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    fName = models.CharField(max_length=50)
    lName = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    jobRole = models.CharField(max_length=20)
    hireDate = models.DateField()
    securityQuestion_Answer1 = models.CharField(max_length=100)
    securityQuestion_Answer2 = models.CharField(max_length=100)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fName', 'lName']

    class Meta:
        abstract = True # this means its an abstract class and should not be used directly

class Engineer(User):
    class Meta:
        db_table = 'Engineer' # creates the table name

class TeamLeader(User):
    class Meta: 
        db_table = 'Team_Leader'

class DepartmentLeader(User):
    class Meta:
        db_table = 'Department_Leader' 

class SeniorManager(User):
    class Meta: 
        db_table = 'Senior_Manager' 

class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=50, unique=True)
    numOfTeams = models.IntegerField()
    deptCreateDate = models.DateField()
    departmentLocation = models.CharField(max_length=50)
    user = models.ForeignKey(DepartmentLeader, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Department' 

class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=20, unique=True)
    numOfMembers = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Team'

class HealthCheckCard(models.Model):
    cardId = models.AutoField(primary_key=True)
    cardName = models.CharField(max_length=50)
    redColorDescrip = models.CharField(max_length=255) # THIS MIGHT CHANGE BECAUSE A 100 IS TOO LIMITED FOR DESCRIP
    greenColorDescrip = models.CharField(max_length=255)

    class Meta:
        db_table = 'HealthCheck_Card' 

class ResultView(models.Model):
    resultId = models.AutoField(primary_key=True)
    summaryType = models.CharField(max_length=50)
    averageProgressScore = models.IntegerField()
    progressOverTime = models.IntegerField() 
    cardProgressSummary = models.CharField(max_length=500)
    teamProgressSummary = models.CharField(max_length=500)
    deptProgressSummary = models.CharField(max_length=500)

    class Meta:
        db_table = 'Result_View'

class HealthCheckResult(models.Model):
    card = models.ForeignKey(HealthCheckCard, on_delete=models.CASCADE)
    result = models.ForeignKey(ResultView, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'HealthCheck_Result' 
        unique_together = (('card', 'result'))


class Session(models.Model):
    sessionId = models.AutoField(primary_key=True)
    sessionDate = models.DateField()
    user = models.ForeignKey('Engineer', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.user and not (
            Engineer.objects.filter(id=self.user.id).exists() or
            TeamLeader.objects.filter(id=self.user.id).exists()
        ):
            raise ValueError("User must be either an Engineer or Team Leader")
        super().save(*args, **kwargs)

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

    class Meta:
        db_table = 'HealthCheck_Vote' 
        unique_together = (('vote', 'card', 'dateCompleted'))