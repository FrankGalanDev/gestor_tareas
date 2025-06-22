from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from backoffice.models import Column, Task, Meeting, MeetingResult


# Display a board with all columns and tasks
   
def home(request):
   
    columns = Column.objects.all()
    return render(request, 'home.html', {'columns': columns})



def dashboard(request):
    meetings = Meeting.objects.all()
    tasks = Task.objects.all()
    results = MeetingResult.objects.all()

    tasks_completed = tasks.filter(meetingresult__completed=True).distinct().count()
    tasks_pending = tasks.count() - tasks_completed
    tasks_total = tasks.count()

    results_completed = results.filter(completed=True).count()
    results_pending = results.count() - results_completed
    results_total = results.count()

    context = {
        'meetings': meetings,
        'tasks_completed': tasks_completed,
        'tasks_pending': tasks_pending,
        'tasks_total': tasks_total,
        'results_completed': results_completed,
        'results_pending': results_pending,
        'results_total': results_total,
    }
    return render(request, 'bases/dashboard.html', context)

