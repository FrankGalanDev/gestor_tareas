from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include 
from django.shortcuts import render
#from django.conf.urls  import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from login.views import registro


from login.views import LoginVista

urlpatterns = [
    path('login/', LoginVista.as_view(), name='login' ),
    path('register/', registro, name="register"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout' ),
     
    
]

