# Co-authored: Student_A_Annie_Moradians, Student_B_Aathika_Ajmal_Basha, Student_C_Mai_Bucheeri, Student_D_Diego_Santos_de_Freitas

from django.contrib import admin
from django.urls import path
from authentication import views as auth_views
from healthCheck import views as formsViews
from results import views as resultsViews
from myAccount import views as accountViews

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    # Navbar
    path('navbar/', auth_views.navbar),
    
    # authentication app URLs
    path('', auth_views.login_view, name='login'), 
    path('createaccount/', auth_views.create_account, name='create_account'), 
    path('securityquestions/', auth_views.security_questions, name='security_questions'),  
    path('resetpassword/', auth_views.reset_password, name='reset_password'), 
    path('securityquestions2/', auth_views.security_questions2, name='security_questions2'),
    path('logout/', auth_views.logout_view, name='log_off'),

    # health check app URLs
    path('healthCheck/chooseSession/', formsViews.chooseSession, name="chooseSession"),
    path('healthCheck/chooseTeam/', formsViews.chooseTeam, name="chooseTeam"),
    path('healthCheck/startPage/', formsViews.startPage, name="startPage"),
    path('healthCheck/healthCheckForm/', formsViews.healthCheckForm, name="healthCheckForm_default"),
    path('healthCheck/healthCheckForm/<int:card_index>', formsViews.healthCheckForm, name="healthCheckForm"),
    path('healthCheck/closingPage/', formsViews.closingPage, name="closingPage"),

    # results app URLs
    path('results/', resultsViews.results, name='results'),
    path('results/submit', resultsViews.results, name='results_submit'),

    # my account app URLs
    path('account/', accountViews.account_view, name='account'),
]
