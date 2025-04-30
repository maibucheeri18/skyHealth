# Author: Student_C_Mai_Bucheeri

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import User
from .models import Department, Team, UserProfile, HealthCheckCard, Session

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('hireDate', 'team', 'is_engineer', 
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
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role_status', 'is_staff')

    def get_role_status(self, obj):
        try:
            profile = obj.profile
            if profile.is_senior_manager:
                return 'Senior Manager'
            elif profile.is_department_leader:
                return 'Department Leader'
            elif profile.is_team_leader:
                return 'Team Leader'
            elif profile.is_engineer:
                return 'Engineer'
            else:
                return 'No role assigned'
        except UserProfile.DoesNotExist:
            return '-'
    get_role_status.short_description = 'Role'

admin.site.unregister(User)
admin.site.register(User, CustomerUserAdmin)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('departmentName', 'numOfTeams', 'departmentLocation', 'deptCreateDate', 'get_department_leader')
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
