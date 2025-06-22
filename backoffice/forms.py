from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.forms.models import inlineformset_factory, modelformset_factory

from django.forms import ModelForm
#from django.forms import TimeInput, TimeField, TextInput, Select, forms, widgets, DateInput, DateField, EmailField
from django.conf import settings
import datetime

from backoffice.models import Column
from backoffice.models import Chat
from backoffice.models import Help
from backoffice.models import Meeting
from backoffice.models import MeetingResult
from backoffice.models import Project
from backoffice.models import Supercolumn
from backoffice.models import Task
from backoffice.models import Team
from backoffice.models import Membership
from accounts.models import CustomUser





class AddUsertoTeamForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all())

    def __init__(self, group_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = CustomUser.objects.exclude(groups__id=group_id)
      
        
'''
class RemoveUserfromTeamForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('group', 'users')
    
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    users = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.none())

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = instance.user_set.all()

'''


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields ="__all__"
        widgets ={
            'project_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del proyecto'}),
            'project_description' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción del proyecto'}),
            'team' : forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

        }
        



class SupercolumnForm(ModelForm):
    class Meta:
        model = Supercolumn
        fields ="__all__"
        widgets ={
            'supercolumn_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Columna superior'}),
            'supercolumn_description' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción de la columna superior'})

        }

class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields ="__all__"
        widgets ={
            'column_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Columna'}),
            'column_description' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripción de la columna'})

        }
   


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields ="__all__"
        widgets ={ 
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tarea'}),
            'description' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
            'column' : forms.Select(attrs={'class':'form-control', 'placeholder':'Columna'}),
            
            'created_by' : forms.Select(attrs={'class':'form-control', 'placeholder':'CREADO POR'}),
            'owner_name' : forms.Select(attrs={'class':'form-control', 'placeholder':'RESPONSABLE'}),
            'task_description' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'DESCRIPCION'}),
            'compliance_date' : forms.DateInput(attrs={'class':'form-control', 'placeholder':'FECHA CUMPLIMIENTO (AAAA-MM-dd)'}),

            'progreso' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'PROGRESO'}),
            'on ' : forms.Select(attrs={'class':'form-control', 'placeholder':'ACTIVA'}),

            'status ' : forms.Select(attrs={'class':'form-control', 'placeholder':'ESTADO'}),
        }
        exclude=['pool_evolucion', 'fechas', 'fecha']
     



class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields ="__all__"
        widgets ={ 
            'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reunion'}),
            'fecha' : forms.DateInput(attrs={'class':'form-control', 'placeholder':'aaaa-mm-dd'}),
            'members' : forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':''}),
            'start_time' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hora de inicio'}),
            'end_time' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hora de finalización'}),
            'objectives ' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Objetivos de la reunión'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
        }
   
    

     
 
class MeetingResultForm(ModelForm):
    class Meta:
        model = MeetingResult
        fields ="__all__"
        widgets ={ 
           ' meeting' : forms.Select(attrs={'class':'form-control', 'placeholder':'Reunión'}),
            'task' : forms.Select(attrs={'class':'form-control', 'placeholder':'Tarea'}),
            'result' : forms.Select(attrs={'class':'form-control', 'placeholder':'Resultado'}),
            'comentarios' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Comentarios'}),
            'completed'  : forms.Select(attrs={'class':'form-control', 'placeholder':'Completada'}),
            'notes' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Notas'}),
            'created_at' : forms.DateInput(attrs={'class':'form-control', 'placeholder':'Fecha de creación'})
        }


class HelpForm(ModelForm):
    class Meta:
        model = Help
        fields = '__all__'
        widgets = {        
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Titulo Ayuda', 'help_text':'Tema'}),
            'subtitle':forms.TextInput(attrs={'class':'form-control','placeholder':'Subitulo:'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Descripcion', 'rows':10}),
            }


class ChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = ['message_topic', 'receiver', 'message_text','message_text']
        widgets = {        
            'message_topic': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Asunto', 'help_text':'Tema'}),
            #'sender':forms.Select(attrs={'class':'form-control','placeholder':'De:'}),
            'receiver':forms.Select(attrs={'class':'form-control','placeholder':'Para:'}),
            'message_text': forms.Textarea(attrs={'class':'form-control','placeholder':'Mensaje', 'rows':10}),
            'message_date': forms.DateInput(format='%d-%m-%Y', attrs={'placeholder':'dd/mm/YYYY'})
             
            }
        exclude=[ 'sender', 'message_reference','message_date']
    
    
class ResponseChatForm(ModelForm):
    class Meta:
        model = Chat
        fields = '__all__'
        widgets = {        
            'message_topic': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Asunto', 'help_text':'Tema'}),
            #'sender':forms.Select(attrs={'class':'form-control','placeholder':'De:'}),
            'receiver':forms.Select(attrs={'class':'form-control','placeholder':'Para:'}),
            'message_text': forms.Textarea(attrs={'class':'form-control','placeholder':'Mensaje', 'rows':10}),
            #'message_date': forms.DateInput(format='%d-%m-%Y', attrs={'placeholder':'dd/mm/YYYY'})
             
            }
        exclude=[ 'sender','message_date','message_reference']


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['user',]

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'members', 'team_description', 'created', 'active',]

MembershipFormSet = inlineformset_factory(Team, Membership, form=MembershipForm, extra=5, can_delete=True)