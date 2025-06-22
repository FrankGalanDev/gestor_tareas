from backoffice.models import Task, Supercolumn, Column, Meeting, MeetingResult, Chat, Project, Team

from datetime import datetime, timedelta, date
from django.utils.timezone import now, localdate
from django.db.models import Q
#from backoffice.mixins import IsSuperuserMixin
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from django.db.models import Count
from django.db.models.functions import TruncMonth



def bulk_data(request): 
    
    

    hoy= date.today()
    mes= hoy.month
    dia = hoy.day


    tarea = None,
    tareas_pendientes = None,
    tareas_vencidas = None,
    tareas_terminadas = None,
    tareas_x_proyectos = None,
    lista_columnas = None,
    reuniones = None,
    proyectos = None,
    resultados = None,
    resultados_terminados = None,
    task_data = []
    bar = []
   
   

    if request.user.is_authenticated:


        #tareas
        Tarea=Task.objects.all()
        tareas = Task.objects.all().count()
        
        tareas_pendientes = Task.objects.filter(on=True).filter(compliance_date__lte=hoy).count()
        tareas_vencidas = Task.objects.filter(on=True).filter(compliance_date__gt=hoy).count()
        tareas_terminadas  = Task.objects.filter(on=False).count()
        a = tareas_terminadas/tareas
        b = tareas_pendientes/tareas
        task_data = [a,b]
        #print(task_data)
        
        print(tareas)

        #columnas
        j=dict()
        clave=[]
        valor=[]
        a = Column.objects.all()
        for i in a:
            j[str(i)]=(Task.objects.filter(column=i)).count()
        
        etiquetas = list(j.keys())
        valores = list(j.values())
        


        

    
        
        #reuniones
        reuniones = Meeting.objects.all().count()

        meetings_by_month = Meeting.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(count=Count('id'))
        meet_months = [meeting['month'].strftime('%Y-%m') for meeting in meetings_by_month]
        meet_counts = [meeting['count'] for meeting in meetings_by_month]
        

        calc_reun = Meeting.objects.annotate(
            mes=TruncMonth('fecha')).values('mes').annotate(cantidad=Count('id')).order_by('mes')
        meses = []
        reun = []
        for re in calc_reun:
            reun.append({
                'cantidad': re['cantidad'] })
            meses.append({
                'mes': re['mes'].strftime('%b %Y'),
            })
        #print(meses, reun)



        #proyectos
        proyectos = Project.objects.all().count()

        calculo = Project.objects.annotate(
            mes=TruncMonth('created_at')).values('mes').annotate(cantidad=Count('id')).order_by('mes')
        moy = []
        proy = []
        for pr in calculo:
            proy.append({
                'cantidad': pr['cantidad'] })
            moy.append({
                'mes': pr['mes'].strftime('%b %Y'),
            })
        #print(moy, proy)

        #equipos
        equipos = Team.objects.filter(active=True).count()
        calc_team = Team.objects.annotate(
            mes=TruncMonth('created')).values('mes').annotate(cantidad=Count('id')).order_by('mes')
        periodo = []
        equipo = []
        for eq in calc_team:
            equipo.append({
                'cantidad': eq['cantidad'] })
            periodo.append({
                'mes': eq['mes'].strftime('%b %Y'),
            })
        print(periodo, equipo)
        
        
        #resultados
        resultados= MeetingResult.objects.all().count()
        resultados_terminados = MeetingResult.objects.filter(completed=True).count()

        #mensajes
        messages = Chat.objects.exclude(status='saved')

        
        return (    
            {
                'tareas': tareas,
                'tareas_pendientes':tareas_pendientes,
                'tareas_vencidas':tareas_vencidas,
                'tareas_terminadas':tareas_terminadas,
                'task_data':task_data,
                #'tareas_x_proyectos':tareas_x_proyectos,
                'lista_columnas':lista_columnas,
                'reuniones':reuniones,
                'proyectos':proyectos,
                'resultados':resultados,
                'resultados_terminados':resultados_terminados,
                'equipos':equipos,
                
                'etiquetas':etiquetas,
                'valores':valores,
                'meet_months':meet_months , 
                'meet_counts': meet_counts,
                
                'moy':moy,
                'proy':proy,
                'meses':meses,  
                'reun':reun,
                'periodo': periodo,
                'equipo':equipo
              
                 
         })
    
    else:
        return ({})    
