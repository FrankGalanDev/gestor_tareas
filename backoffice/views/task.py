
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.db.models import Count
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import json
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Trunc
from django.db.models import Max
import io
from io import BytesIO
import ast
from ast import literal_eval
import urllib, base64
from django.templatetags.static import static
from django.views.generic import  ListView, DetailView, View
from django.views.generic.edit import  CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import Context, loader 
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from backoffice.forms import TaskForm
from backoffice.models import Task, Column
from accounts.models import CustomUser
from django.core.paginator import Paginator
from django.utils import timezone

from datetime import datetime, timedelta
from datetime import timedelta



#CRUD
class TaskList(LoginRequiredMixin,  ListView):
    model = Task
    paginate_by = 10
    template_name = 'tasks/all_tasks.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Task.objects.filter(
                Q(created_by__name__icontains=search)| 
                Q(created_by__last_name__icontains=search)|
                Q(created_by__first_name__icontains=search)|
                Q(created_by__username__icontains=search)|
                Q(task_name__icontains=search)|  
                Q(owner_name__name__icontains=search)| 
                Q(owner_name__last_name__icontains=search)|
                Q(owner_name__first_name__icontains=search)|
                Q(owner_name__username__icontains=search)|
                Q(compliance_date__icontains=search)| 
                Q(task_description__icontains=search)| 
                Q(status__icontains=search) 
                ).distinct()            
            
        else:
             Task.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tareas'
        context['table_title'] = 'Lista de tareas'
        context['table_subtitle'] = 'Todas las tareas'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/new_task.html' 

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Tareas'
        context['table_title'] = 'Nueva tarea'
        context['table_subtitle'] = 'Añada una tarea'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_tasks')



class TaskDetail(DetailView):
    model = Task
    template_name = 'tasks/detail_task.html'
    success_url = reverse_lazy('all_tasks')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        chart_data = task.get_chart_data()
        context['chart_data'] = chart_data
        #print(context)
        return context




class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('all_tasks')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tareas'
        context['table_title'] = 'Editar tarea'
        context['table_subtitle'] = 'Modificar tarea'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('all_tasks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tareas'
        context['table_title'] = 'Eliminar tarea'
        context['table_subtitle'] = 'Borre un tarea'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)





 
@csrf_protect
def actualizar_tablero(request):
    
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        column_id = request.POST.get('column_id')

        try:
            task = Task.objects.get(id=task_id)
            column = Column.objects.get(id=column_id) # Obtiene la instancia de Column correspondiente
            task.column = column # Asigna la instancia de Column a la columna de la tarea
            task.save()
            return JsonResponse({'status': 'ok'})
            return JsonResponse({'task_id': task_id, 'column': column}, safe=False)

        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'msg': 'La tarea no existe'})
    else:
        return JsonResponse({'status': 'error', 'msg': 'Error'})




class TaskProgressView(View):
    def get(self, request, task_id):
        tarea = Task.objects.get(pk=task_id)
        progreso = tarea.progreso

        # Crear gráfico de barras
        x = ['Progreso']
        y = [progreso]
        plt.bar(x, y)
        plt.title(tarea.nombre)
        plt.xlabel('Progreso')
        plt.ylabel('Porcentaje')
        plt.ylim(0, 100)
        plt.savefig('grafico.png')
        plt.close()

        with open('grafico.png', 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = 'inline; filename=grafico.png'
            return response
       
            #return render(request, 'tasks/task_progress.html', context)





class TaskProgressView(View):
    def get(self, request, id, *args, **kwargs):
        template_name= 'dashboards/grafico_lineas.html'
        model =Task

        # Obtener todas las tareas
        tarea = Task.objects.filter(id =id)
        fechas = to_string(self.tareas.pool_date)
        ''' 
        # Crear una lista de fechas y una lista de valores para cada tarea
        task_data = []
        for c in tarea.time_progress:
            # Obtener todo los cambios de progreso de la tarea
            progress_updates = task.progressupdate_set.all()
            # Crear una lista de fechas y una lista de valores para las actualizaciones de progreso
            dates = []
            values = []
            for update in progress_updates:
                dates.append(update.fecha)
                values.append(update.valor)
            # Agregar las listas de fechas y valores al conjunto de datos de la tarea
        '''
        task_data.append((tarea.task_name, fechas, tarea.time_progress))

        # Crear una figura de Matplotlib con un gráfico de línea para cada tarea
        fig, ax = plt.subplots()
        for task in task_data:
            ax.plot(task[1], task[2], label=task[0])
        
        # Configurar la etiqueta del eje x
        ax.set_xlabel('Fechas')
        ax.xaxis.set_major_formatter(plt.DateFormatter('%Y-%m-%d'))

        # Configurar la etiqueta del eje y
        ax.set_ylabel('Progreso')

        # Configurar el título del gráfico
        ax.set_title('Progresión de tareas')

        # Agregar la leyenda al gráfico
        ax.legend()

        # Guardar la figura en un buffer de memoria
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Convertir la imagen en un objeto HttpResponse para mostrarla en el navegador
        return HttpResponse(image_png, content_type='image/png')




def task_progress(request):
    # Calcula el número de tareas completadas, pendientes y en progreso
    completed_tasks = Task.objects.filter(status='completed').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    in_progress_tasks = Task.objects.filter(status='in_progress').count()

    # Configura el gráfico de barras
    labels = ['Completadas', 'Pendientes', 'En progreso']
    values = [completed_tasks, pending_tasks, in_progress_tasks]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    plt.bar(labels, values, color=colors)
    plt.title('Progreso de tareas')

    # Convierte el gráfico en una imagen y lo envía al template
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # Renderiza el template con el gráfico de barras
    return render(request, 'task_progress.html', {'plot_url': plot_url})


#GRAPHS

def task_stats(request):
    columns = Column.objects.annotate(num_tasks=Count('task'))
    labels = [column.name for column in columns]
    values = [column.num_tasks for column in columns]

    fig = plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.title('Tasks by Column')
    plt.xlabel('Column')
    plt.ylabel('Number of Tasks')

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'task_stats.html', {'graphic': graphic})


#Grafico de puntos (scatter)
def task_status_scatter(request):
    tasks = Task.objects.all()
    data = [(task.created_at, task.updated_at, task.column.name) for task in tasks]

    fig, ax = plt.subplots(figsize=(8, 6))
    for column in Column.objects.all():
        column_data = [(task.created_at, task.updated_at) for task in tasks.filter(column=column)]
        x = [task[0] for task in column_data]
        y = [task[1] for task in column_data]
        ax.scatter(x, y, label=column.name)

    ax.set_title('Task Status')
    ax.set_xlabel('Created At')
    ax.set_ylabel('Updated At')
    ax.legend()

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'task_status_scatter.html', {'graphic': graphic})


# Grafico de lineas (lines)
def task_status_line(request):
    tasks = Task.objects.all()
    data = [(task.created_at, task.updated_at, task.column.name) for task in tasks]

    fig, ax = plt.subplots(figsize=(8, 6))
    for column in Column.objects.all():
        column_data = [(task.created_at, task.updated_at) for task in tasks.filter(column=column)]
        x = [task[0] for task in column_data]
        y = [task[1] for task in column_data]
        ax.plot(x, y, label=column.name)

    ax.set_title('Task Status')
    ax.set_xlabel('Created At')
    ax.set_ylabel('Updated At')
    ax.legend()

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'task_status_line.html', {'graphic': graphic})


'''
Return a list with the number of tasks in each status and the average duration for each status
'''
def task_statistics_data():
   
    # Get all columns
    columns = Column.objects.all()

    data = []
    for column in columns:
        tasks = Task.objects.filter(column=column)
        data.append({
            'column': column.name,
            'tasks_count': tasks.count(),
            'average_duration': tasks.aggregate(Avg('duration'))['duration__avg'] or 0
        })

    return data



#Aquí creamos una lista scatter_data que contiene un diccionario para cada columna, 
# que tiene las mismas claves que en la función task_statistics_data(), más una clave 
# adicional 'name' que es el nombre de la columna. Luego usamos esta lista para generar el 
# gráfico de puntos con la función create_scatter_chart().

#Finalmente, agregamos los datos necesarios para el gráfico de líneas a la variable line_data, 
# y usamos esta variable para generar el gráfico de líneas con la función create_line_chart().

#Con estas actualizaciones, ahora podemos ver el estado de nuestras tareas en gráficos de puntos y 
# de líneas en las URLs status/scatter/ y status/line/ respectivamente.

def task_statistics(request):
    # Get data for the scatter chart
    data = task_statistics_data()
    scatter_data = [{
        'x': d['tasks_count'],
        'y': d['average_duration'],
        'name': d['column']
    } for d in data]

    # Get data for the line chart
    line_data = {
        'labels': [d['column'] for d in data],
        'tasks_count': [d['tasks_count'] for d in data],
        'average_duration': [d['average_duration'] for d in data],
    }

    # Generate the charts
    scatter_chart = create_scatter_chart(scatter_data)
    line_chart = create_line_chart(line_data)

    # Render the template
    return render(request, 'task_statistics.html', {
        'scatter_graphic': scatter_chart,
        'line_graphic': line_chart,
    })





#Este código creará un gráfico que muestra la evolución de la tarea a través del tiempo utilizando 
# la información almacenada en la variable evolucion. Luego, guarda el gráfico como un archivo PNG y 
# lo muestra en la plantilla task_detail.html.

def progreso(request, pk):
    task = get_object_or_404(Task, pk=pk)
    evolucion = json.loads(task.evolucion)
    fechas = []
    progreso = []
    for registro in evolucion:
        fechas.append(registro['fecha'])
        progreso.append(registro['progreso'])
    plt.plot(fechas, progreso)
    plt.xlabel('Fecha')
    plt.ylabel('Progreso')
    plt.title('Evolución de tarea')
    plt.grid(True)
    plt.savefig('grafico.png')
    with open('grafico.png', 'rb') as f:
        grafico = f.read()
    return render(request, 'tasks/task_progress.html', {'task': task, 'grafico': grafico})







