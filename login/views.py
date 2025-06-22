from turtle import title
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, login, authenticate
from login.forms import userRegistrationForm
from django.conf import settings

from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from accounts.forms import CustomUserForm
from django.core.mail import send_mail
from django.conf import settings
from accounts.forms import CustomUserCreationForm


# Create your views here.
class LoginVista(LoginView):
    template_name = 'access/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #return redirect('/backend/backend/')
            return redirect(settings.LOGIN_REDIRECT_URL)
            
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [title]= 'Iniciar sesion'
        return context



# Create your views here.
def registro(request):
    
    if request.user.is_authenticated:
       return redirect('dashboard')

    data={
        'form':userRegistrationForm()
    }
    
    if request.method == "POST":
        formulario = userRegistrationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
             
            username=formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        else:
            for error in list(formulario.errors.values()):
                print(request, error)
                
        
    return render(
        request,
        'access/register.html',
        data
    )
