from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.models import inlineformset_factory, modelformset_factory
from accounts.models import CustomUser
from django.forms import ModelForm
#from django.forms import TimeInput, TimeField, TextInput, Select, forms, widgets, DateInput, DateField, EmailField
from django.conf import settings
import datetime


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')





class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        #costumizing the date input values
        #birthday_data = DateField(input_formats=settings.DATE_INPUT_FORMATS, required=False) 
        widgets = {
            'username' :forms.TextInput(attrs={'class':'form-control','placeholder':'Apodo:'}),
            'name' :forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el nombre de usuario:'}),

            'photo' : forms.ClearableFileInput(attrs={'class':'form-control','placeholder':'Imagen'}), 
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el primer apellido::'}), 
            'last_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el segundo apellido:'}),    
            'phone ': forms.TextInput(attrs={'class':'form-control','placeholder':'Escriba el teléfono'}),
            'email' : forms.EmailInput(attrs={'class':'form-control','placeholder':'Escriba el email'}),
            'rol' : forms.Select(attrs={'class':'form-control','placeholder':'Introduzca el rol'})           
            }
        exclude = ['groups', 'user_permissions','last_login',' is_staff', 'is_active']
