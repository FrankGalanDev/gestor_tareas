from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from backoffice.models import Column, Task, Meeting, MeetingResult
from django.views.generic import TemplateView




class KanbanBoardView(TemplateView):
    template_name = "dashboards/kanban_board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requested_cards"] = Task.objects.filter(column=1).filter(on = True)
        context["ready_cards"] = Task.objects.filter(column=2).filter(on = True)
        context["in_process_cards"] = Task.objects.filter(column=3).filter(on = True)
        context["done_cards"] = Task.objects.filter(column=4).filter(on = True)
        return context
       



def dashboard_dos(request):
    # Obtener las tareas y resultados de reuniones
    tareas = Task.objects.all()
    reuniones = Meeting.objects.all()

    # Obtener el número de tareas completadas y no completadas
    tareas_completadas = tareas.filter(completada=True).count()
    tareas_no_completadas = tareas.filter(completada=False).count()

    # Obtener la cantidad de resultados positivos y negativos de las reuniones
    resultados_positivos = reuniones.filter(resultado='positivo').count()
    resultados_negativos = reuniones.filter(resultado='negativo').count()

    # Obtener el progreso de las tareas
    progreso_tareas = tareas.annotate(
        mes=TruncMonth('fecha_creacion')
    ).values('mes').annotate(
        completadas=Count('id', filter=Q(completada=True)),
        no_completadas=Count('id', filter=Q(completada=False)),
    )

    # Obtener el resultado de las reuniones
    resultado_reuniones = reuniones.annotate(
        mes=TruncMonth('fecha_reunion')
    ).values('mes').annotate(
        positivos=Count('id', filter=Q(resultado='positivo')),
        negativos=Count('id', filter=Q(resultado='negativo')),
    )

    context = {
        'tareas_completadas': tareas_completadas,
        'tareas_no_completadas': tareas_no_completadas,
        'resultados_positivos': resultados_positivos,
        'resultados_negativos': resultados_negativos,
        'progreso_tareas': progreso_tareas,
        'resultado_reuniones': resultado_reuniones,
    }

    return render(request, 'dashboard_dos.html', context)
