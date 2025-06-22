from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from backoffice.models import Column, Task, Meeting, MeetingResult


#Create a scatter chart with the given data and return it as a base64-encoded PNG image.

def create_scatter_chart(data):   
   
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    for d in data:
        ax.scatter(d['x'], d['y'], label=d['name'])
    ax.set_xlabel('Number of Tasks')
    ax.set_ylabel('Average Duration')
    ax.legend()
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return data


#Create a line chart with the given data and return it as a base64-encoded PNG image.

def create_line_chart(data):
        
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(data['labels'], data['tasks_count'], label='Tasks Count')
    ax.plot(data['labels'], data['average_duration'], label='Average Duration')
    ax.set_xlabel('Column')
    ax.set_ylabel('Value')
    ax.legend()
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return data



def scatter_chart(request):

#Display a scatter chart of the average duration of tasks in each column, grouped by column name

    data = []
    for column in Column.objects.all():
        tasks = Task.objects.filter(column=column)
    if tasks:
        data.append({
            'x': tasks.count(),
            'y': tasks.aggregate(Avg('duration'))['duration__avg'],
            'name': column.name
            })
    chart = create_scatter_chart(data)
    return render(request, 'scatter_chart.html', {'chart': chart})



#Display a line chart of the number of tasks and average duration of tasks in each column, grouped by column name

def line_chart(request):

    data = {
    'labels': [],
    'tasks_count': [],
    'average_duration': []
    }
    for column in Column.objects.all():
        tasks = Task.objects.filter(column=column)
        data['labels'].append(column.name)
        data['tasks_count'].append(tasks.count())
        data['average_duration'].append(tasks.aggregate(Avg('duration'))['duration__avg'])
        chart = create_line_chart(data)
    return render(request, 'line_chart.html', {'chart': chart})



#En este código, usamos la librería Matplotlib para crear un gráfico de barras que muestre 
# el número de tareas completadas, pendientes y en progreso. Configuramos los datos del gráfico 
# y los colores, lo convertimos en una imagen y lo enviamos al template.

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
