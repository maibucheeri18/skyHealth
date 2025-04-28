"""
URL configuration for skyHealth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

This file defines all the application-level URLs and maps them to their corresponding views.
"""

# Author: Student_D_Diego_Santos_de_Freitas 

from django.contrib import admin
from django.urls import path

from healthCheck import views as formsViews
from authentication import views as auth_views


urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    path('healthCheck/chooseSession/', formsViews.chooseSession, name="chooseSession"),
    path('healthCheck/chooseTeam/', formsViews.chooseTeam, name="chooseTeam"),
    path('healthCheck/startPage/', formsViews.startPage, name="startPage"),
    path('healthCheck/healthCheckForm/', formsViews.healthCheckForm, name="healthCheckForm_default"),
    path('healthCheck/healthCheckForm/<int:card_index>', formsViews.healthCheckForm, name="healthCheckForm"),
    path('healthCheck/closingPage/', formsViews.closingPage, name="closingPage")
    
    # Authentication URLs
    path('login/', auth_views.login_view, name='login'),  # User login page
    path('createaccount/', auth_views.create_account, name='create_account'),  # New account registration
    
    # Password recovery flow URLs
    path('securityquestions/', auth_views.security_questions, name='security_questions'),  # Forgotten password security questions
    path('resetpassword/', auth_views.reset_password, name='reset_password'),  # Password reset form
    
    # Account setup URLs
    path('securityquestions2/', auth_views.security_questions2, name='security_questions2'),  # New account security questions setup
    
    # Application URLs
    path('dashboard/', auth_views.dashboard, name='dashboard'),  # Main dashboard page
]