"""
URL configuration for skyHealth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login_view, name='login'),
    path('securityquestions/', auth_views.security_questions, name='security_questions'),
    path('resetpassword/', auth_views.reset_password, name='reset_password'),
    path('createaccount/', auth_views.create_account, name='create_account'),
    path('securityquestions2/', auth_views.security_questions2, name='security_questions2'),
    path('dashboard/', auth_views.dashboard, name='dashboard')
]
