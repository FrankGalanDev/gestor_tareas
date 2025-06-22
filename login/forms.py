from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.forms import ModelForm
#from django.forms import TimeInput, TimeField, TextInput, Select, forms, widgets, DateInput, DateField, EmailField
from django.conf import settings
import datetime

from accounts.models import CustomUser

class userRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username','email','name','first_name','last_name', 'password1', 'password2']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Apodo'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Primer apellido'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Segundo apellido'}),

            'password1':forms.PasswordInput(attrs={'class':'form-control','placeholder':' Escriba su contraseña'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Repita su contraseña'}),
         }
        exclude =['name','first_name','last_name' ]
''' 
    def save(self, commit=True):
        user = super(userRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data({'email'})
        if commit:
            user.save()
        return user
        '''