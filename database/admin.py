from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import User
from .models import (
    Department, Team, UserProfile, HealthCheckCard, 
    Session, Vote, HealthCheckVote
)

class UserProfileForm(forms.ModelForm):
    JOB_ROLE_CHOICES = [
        ('Engineer', 'Engineer'),
        ('Team Leader', 'Team Leader'),
        ('Department Leader', 'Department Leader'),
        ('Senior Manager', 'Senior Manager'),
    ]

    jobRole = forms.ChoiceField(choices=JOB_ROLE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ( 'jobRole', 'hireDate', 'team', 'is_engineer', 
        'is_team_leader','is_department_leader', 'is_senior_manager', 
        'securityQuestion_Answer1', 'securityQuestion_Answer2'
        )

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileForm
    can_delete = False
    verbose_name_plural = 'User Profiles'

class CustomerUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_job_role', 'is_staff')
    list_filter = ('profile__jobRole',)

    def get_job_role(self, obj):
        try:
            return obj.profile.jobRole
        except UserProfile.DoesNotExist:
            return '-'
    get_job_role.short_description = 'Job Role'

admin.site.unregister(User)
admin.site.register(User, CustomerUserAdmin)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentName', 'numOfTeam', 'departmentLocation', 'deptCreateDate', 'get_department_leader')
    search_fields = ('departmentName',)

    def get_department_leader(self, obj):
        if obj.leader:
            return f"{obj.leader.first_name} {obj.leader.last_name}"
        return 'None'
    get_department_leader.short_description = 'Department Leader'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('teamName', 'numOfMembers', 'department', 'get_team_leader')
    search_fields = ('teamName',)
    list_filter = ('department',)

    def get_team_leader(self, obj):
        if obj.leader:
            return f"{obj.leader.first_name} {obj.leader.last_name}"
        return 'None'
    get_team_leader.short_description = 'Team Leader'

@admin.register(HealthCheckCard)
class HealthCheckCardAdmin(admin.ModelAdmin):
    list_display = ('cardId', 'cardName', 'redColorDescrip', 'greenColorDescrip')
    search_fields = ('cardName',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('sessionId', 'sessionDate', 'user')
    list_filter = ('sessionDate',)
    search_fields = ('user__username',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('voteId', 'voteColour', 'progressIndicator', 'session')
    list_filter = ('voteColour', 'progressIndicator')
    search_fields = ('voteComment',)

@admin.register(HealthCheckVote)
class HealthCheckVoteAdmin(admin.ModelAdmin):
    list_display = ('vote', 'card', 'dateCompleted', 'user', 'team', 'department')
    list_filter = ('dateCompleted', 'team', 'department')
    search_fields = ('user__username',)