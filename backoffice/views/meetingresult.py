from django.shortcuts import render, get_object_or_404, redirect
from backoffice.models import MeetingResult, Meeting, MeetingResult
from backoffice.forms import MeetingResultForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.templatetags.static import static
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import  CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.template import Context, loader 
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from accounts.models import CustomUser 
from django.core.paginator import Paginator




class MeetingResultList(ListView):
    model = MeetingResult
    template_name = 'all_meetingresults.html'

    template_name = 'meetingresults/all_meetingresults.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return MeetingResult.objects.filter(
                Q(column_name__icontains=search)| 
                Q(column_description__icontains=search)|
                Q(meeting__icontains=search)|
                Q(task__icontains=search)|
                Q(result__icontains=search)|
                Q(completed__icontains=search)|
                Q(notes__icontains=search)|
                Q(created_at__icontains=search)
              
                ).distinct()            
            
        else:
             MeetingResult.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Resultados por reunion'
        context['table_title'] = 'Lista de columnas'
        context['table_subtitle'] = 'Todas las columnas'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MeetingResultDetail(DetailView):
    model = MeetingResult
    template_name = 'detail_meetingresult.html'
    success_url = reverse_lazy('all_meetingresults')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resultados por reuniones'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles de la reunion'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)




class MeetingResultCreate(CreateView):
    model = MeetingResult
    form_class = MeetingResultForm
    template_name = 'meetingresults/new_meetingresults.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Resultados por Reunion'
        context['table_title'] = 'Nuevo'
        context['table_subtitle'] = 'Añadir'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_meetingresults')



class MeetingResultUpdate(UpdateView):
    model = MeetingResult
    form_class = MeetingResultForm
    template_name = 'update_meetingresult.html'
    success_url = reverse_lazy('all_meetingresults')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resultados por reuniones'
        context['table_title'] = 'Editar'
        context['table_subtitle'] = 'Modificar el resultado'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MeetingResultDelete(DeleteView):
    model = MeetingResult
    success_url = reverse_lazy('all_meetingresults')    
    template_name = 'delete_meetingresult.html'
  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Resultados por reuniones'
        context['table_title'] = 'Eliminar '
        context['table_subtitle'] = 'Borre '
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
