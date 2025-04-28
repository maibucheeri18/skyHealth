"""
URL configuration for skyHealth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

This file defines all the application-level URLs and maps them to their corresponding views.
"""

from django.contrib import admin
from django.urls import path
from authentication import views as auth_views
from healthCheck import views as formsViews
from results import views as resultsViews
from myAccount import views as accountViews

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    
    # authentication app URLs
    path('login/', auth_views.login_view, name='login'), 
    path('createaccount/', auth_views.create_account, name='create_account'), 
    path('securityquestions/', auth_views.security_questions, name='security_questions'),  
    path('resetpassword/', auth_views.reset_password, name='reset_password'), 
    path('securityquestions2/', auth_views.security_questions2, name='security_questions2'),

    # health check app URLs
    path('healthCheck/chooseSession/', formsViews.chooseSession, name="chooseSession"),
    path('healthCheck/chooseTeam/', formsViews.chooseTeam, name="chooseTeam"),
    path('healthCheck/startPage/', formsViews.startPage, name="startPage"),
    path('healthCheck/healthCheckForm/', formsViews.healthCheckForm, name="healthCheckForm_default"),
    path('healthCheck/healthCheckForm/<int:card_index>', formsViews.healthCheckForm, name="healthCheckForm"),
    path('healthCheck/closingPage/', formsViews.closingPage, name="closingPage"),

    # results app URLs
    path('results/', resultsViews.results, name='results'),

    # my account app URLs
    path('account/', accountViews.account_view, name='account'),
]
