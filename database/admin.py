from django.contrib import admin

from database.models import (
    Engineer, TeamLeader, DepartmentLeader, SeniorManager, 
    Department, Team,  HealthCheckVote, Vote, HealthCheckCard, Session
)

# Register your models here.
class EngineerInline(admin.StackedInline):
    model = Engineer
    extra = 1
    fields = ('username', 'fName', 'lName', 'email')
    verbose_name = "Team Member"
    verbose_name_plural = "Team Members"

class TeamInline(admin.StackedInline):
    model = Team
    extra = 1
    fields = ('teamName', 'numOfMembers', 'leader')
    show_change_link = True

@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('username', 'fName', 'lName', 'email', 'team')
    search_fields = ('username', 'fName', 'lName', 'email')
    list_filter = ('team',)

    fields = (
        'fName', 'lName', 'username', 'email', 'hireDate', 
        'securityQuestion_Answer1', 'securityQuestion_Answer2','team', 
    )

@admin.register(TeamLeader)
class TeamLeaderAdmin(admin.ModelAdmin):
    list_display = ('username', 'fName', 'lName', 'email')
    search_fields = ('username', 'fName', 'lName', 'email')

    fields = (
        'fName', 'lName', 'username', 'email', 'hireDate', 
        'securityQuestion_Answer1', 'securityQuestion_Answer2',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(led_team__isnull=False)

@admin.register(DepartmentLeader)
class DepartmentLeader(admin.ModelAdmin):
    list_display = ('username', 'fName', 'lName', 'email')
    search_fields = ('username', 'fName', 'lName', 'email')

    fields = (
        'fName', 'lName', 'username', 'email', 'hireDate', 
        'securityQuestion_Answer1', 'securityQuestion_Answer2',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(led_department__isnull=False)


@admin.register(SeniorManager)
class SeniorManager(admin.ModelAdmin):
    fields = (
        'fName', 'lName', 'username', 'email', 'hireDate', 
        'securityQuestion_Answer1', 'securityQuestion_Answer2',
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('teamName', 'numOfMembers', 'department', 'leader')
    list_filter = ('department',)
    search_fields = ('teamName',)
    inlines = [EngineerInline]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentName', 'numOfTeams', 'departmentLocation', 'leader')
    search_fields = ('departmentName',)
    inlines = [TeamInline]

@admin.register(HealthCheckVote)
class HealthCheckVoteAdmin(admin.ModelAdmin):
    list_display = ('vote', 'card', 'team', 'department')
    search_fields = ('card',)
    fields = ('vote', 'card', 'dateCompleted', 'team', 'department')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voteColour', 'voteComment')
    search_fields = ('voteColour',)
    fields = ('voteColour', 'progressIndicator', 'voteComment', 'session')

@admin.register(HealthCheckCard)
class HealthCheckCardAdmin(admin.ModelAdmin):
    list_display = ('cardId', 'cardName')
    search_fields = ('cardName',)
    fields = ('cardName', 'redColorDescrip', 'greenColorDescrip')

@admin.register(Session) 
class SessionAdmin(admin.ModelAdmin):
    list_display = ('sessionId', 'sessionDate')
    list_filter = ('sessionDate',)
    fields = ('sessionDate',)