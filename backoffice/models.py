from django.db import models
#from django.contrib.postgres.fields import ArrayField #para añadir un array como campo
from django.db.models import JSONField
from django.core.validators import MaxValueValidator #permite establecer valores maximos
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta, date
from django.urls import  reverse, reverse_lazy
import json
from enum import unique
from django.db.models import Count
from secrets import choice  
from tkinter import CASCADE
from django.dispatch import receiver
from django.db.models import Sum
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from django.conf import settings
from tasker.settings import MEDIA_URL, STATIC_URL
from django.db.models.signals import post_save, pre_delete, pre_save



MESSAGE_STATUS = (
    ('leido' , 'leido'),
    ('para_recordar' , 'para recordar'),
    ('sin leer', 'sin leer'),
    
)


CustomUser = get_user_model()

#===PROJECT MODEL===
class Project(models.Model):
    project_name = models.CharField('Proyecto',   max_length=100)
    project_description = models.TextField('DESCRIPCION', blank=True, null=True)
    active = models.BooleanField('Abierto', default=True)
    created_at = models.DateTimeField()


    def __str__(self):
        return self.project_name
    
    class Meta:
        ordering = ['project_name']


    def all_projects_by_month(request):
        projects_by_month = Project.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id'))
        months = [project['month'].strftime('%Y-%m') for project in projects_by_month]
        counts = [project['count'] for project in projects_by_month]
        context = {
            'months': months,
            'counts': counts,
        }

    def get_absolute_url(self):
        return reverse('all_projects.html', kwargs={'pk':self.id})





#===SUPER COLUMN MODEL===
class Supercolumn(models.Model):
    #foreing key
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default='')
    supercolumn_name = models.CharField('Supercolumna',   max_length=100)
    supercolumn_description = models.TextField('DESCRIPCION', blank=True, null=True)

    def __str__(self):
        return self.supercolumn_name
    
    class Meta:
        ordering = ['supercolumn_name']

    def get_absolute_url(self):
        return reverse('all_supercolumns.html', kwargs={'pk':self.id})



#===COLUMN MODEL===
class Column(models.Model):
    #foreing key
    superior = models.ForeignKey(Supercolumn, verbose_name= 'Superior', on_delete=models.CASCADE, blank=True, null=True)
    column_name = models.CharField(
        'Columna',        
        max_length=100)
    column_description = models.TextField('DESCRIPCION', blank=True, null=True)

    def __str__(self):
        return self.column_name
    
    class Meta:
        ordering = ['column_name']

    def get_absolute_url(self):
        return reverse('all_columns.html', kwargs={'pk':self.id})




#===TASK MODEL===
class Task(models.Model):

    task_name= models.CharField('TAREA', max_length=100)
    
    #foreing keys
    column = models.ForeignKey(Column,verbose_name='Columna',  on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, verbose_name='CREADA POR', on_delete=models.CASCADE )
    owner_name = models.ForeignKey(CustomUser, verbose_name='RESPONSABLE',  on_delete=models.CASCADE, related_name='responsable')
    project = models.ForeignKey(Project, verbose_name='Proyecto', default=1, on_delete=models.CASCADE)
    
    pool_evolucion = models.JSONField(verbose_name='Evolucion', default=dict)
    
    task_description = models.TextField('DESCRIPCION', blank=True, null=True)
    compliance_date = models.DateTimeField('FECHA DE CUMPLIMIENTO', blank=True, null=True, default=datetime.now)
    progreso = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    on = models.BooleanField('Activar',default=True)

    
    def get_time_diff(self):
        
        now = datetime.now() #obteniendo fecha actual 
        
        #convirtiendo  fechas a string
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
        meta = datetime.strftime(self.compliance_date, "%m/%d/%Y, %H:%M:%S")

        #pasamos string a date
        ahora = datetime.strptime(date_time, "%m/%d/%Y, %H:%M:%S")
        fecha_tope = datetime.strptime(meta, "%m/%d/%Y, %H:%M:%S")

        restante = fecha_tope - ahora
        return restante.days
     

    def save(self, *args, **kwargs):
        evento=dict()
        now = datetime.now()
        print(now,'now')

        ahora =str(now)
        print( ahora,'ahora-string')

        ahora = ahora[:-7]
        print(ahora, 'ahora menos 7')

        evento[ahora] = self.progreso
        print(evento,'evento bien')

        for k in evento.keys():
            clave=k
        
        for v in evento.values():
            valor=v

        # agrega el evento al diccionario pool_evolucion
        self.pool_evolucion[clave]=valor

        print(self.pool_evolucion,'final')
        
        super().save(*args, **kwargs)



    def get_chart_data(self):
        # Obtener los datos necesarios para el gráfico
        labels = []
        data = []
        for key, value in self.pool_evolucion.items():
            labels.append(key)
            data.append(value)
            
        return {'labels': labels, 'data': data}

    class Meta:
        ordering = ['compliance_date']
    
    def __str__(self):
        return self.task_name
    
    def get_absolute_url(self):
        return reverse('all_tasks.html', kwargs={'pk':self.id})






class Help(models.Model): 
    
    title = models.CharField('Titulo', max_length=200, blank=True, null=True)
    subtitle = models.CharField('SubTitulo', max_length=200, blank=True, null=True)
    description = models.TextField('Descripción',  blank=True, null=True)
    
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('help.html', kwargs={'pk':self.id})
    
    class Meta:
        verbose_name='Ayuda'
        verbose_name_plural='Ayuda'




# ----- INTERNAL MESSAGES MODEL ------
class Chat(models.Model): 
    #FOREIGN KEY
    sender = models.ForeignKey(CustomUser, verbose_name='CREADO POR:', on_delete=models.CASCADE, related_name='messages', default='0')
    receiver = models.ForeignKey(CustomUser, verbose_name='DESTINATARIO:', on_delete=models.CASCADE, related_name='receiver')
  

    message_topic= models.CharField('ASUNTO:', max_length=30)
    message_reference = models.CharField('Previo', max_length=100, blank=True, null=True)
    message_text= models.TextField('MENSAJE:', blank=True, null=True)
    message_date = models.DateTimeField('FECHA:', auto_now_add=True, blank=True, null=True)
    status = models.CharField(
        'Estado del mensaje',
        choices=MESSAGE_STATUS,  
        max_length=31, 
        blank=True, 
        null=True,
        default='sin leer'
        )
    
    def tiempo(self):
        now = datetime.now()

        message_date_time = now.strftime("%m/%d/%Y, %H:%M:%S") 
        sent = datetime.strftime(self.message_date, "%m/%d/%Y, %H:%M:%S")

        ahora = datetime.strptime(message_date_time, "%m/%d/%Y, %H:%M:%S")
        enviado = datetime.strptime(sent, "%m/%d/%Y, %H:%M:%S")
        
        tiempo = ahora - enviado
        return tiempo
    
    
    
    class Meta:
        ordering = ['message_date']

    def __str__(self):
        return self.message_topic
       
    
    def get_absolute_url(self):
        return reverse('all_chats.html', kwargs={'pk':self.id})   



class Team(models.Model):
    #foreing key
    members = models.ManyToManyField(CustomUser, through='Membership', related_name='teams')
    team_name = models.CharField('Nombre del equipo', max_length=100)
    team_description = models.TextField('Descripción y objetivos del equipo', blank=True, null=True)
    created = models.DateField()
    active = models.BooleanField(default=True)


    def meetings_per_month(self):
        meetings = Meeting.objects.filter(team=self).annotate(month=TruncMonth('fecha')).values('month').annotate(count=Count('id')).order_by('month')
        return [(m['month'].strftime('%b %Y'), m['count']) for m in meetings]

    class Meta:
        ordering =['team_name']

    def __str__(self):
        return self.team_name
    
    def get_absolute_url(self):
        return reverse("all_teams", kwargs={"pk": self.pk})
    


class Membership(models.Model):
    #foreing key
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField('Jefe del Equipo', default=False)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("all_members", kwargs={"pk": self.pk})



class Meeting(models.Model):
    #foreing keys
    team = models.ForeignKey(Team, verbose_name='Equipos', default=1, on_delete=models.CASCADE)

    nombre = models.CharField('Nombre de la reunión', max_length=200,)
    fecha = models.DateTimeField()
    descripcion = models.TextField('Descripcion de la reunión', blank=True, null=True)
    start_time = models.CharField('Hora Inicio',max_length= 20,  blank=True, null=True)
    end_time = models.CharField('Hora Finalización', max_length= 20, blank=True, null=True)
    objectives = models.TextField('Objetivos', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('all_meetings', args=[str(self.id)])


    
    def meetings_per_month(self):
        meetings = Meeting.objects.filter(team=self).annotate(month=TruncMonth('fecha')).values('month').annotate(count=Count('id')).order_by('month')
        return [(m['month'].strftime('%b %Y'), m['count']) for m in meetings]

    def all_meetings_by_month(request):
        meetings_by_month = Meeting.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(count=Count('id'))
        months = [meeting['month'].strftime('%Y-%m') for meeting in meetings_by_month]
        counts = [meeting['count'] for meeting in meetings_by_month]
        context = {
            'months': months,
            'counts': counts,
        }
        return render(request, 'meetings_by_month.html', context)



class MeetingResult(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comentarios = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.meeting.nombre} - {self.task_name}"
    
    def get_absolute_url(self):
        return reverse('all_meetingresults.html', args=[str(self.id)])


