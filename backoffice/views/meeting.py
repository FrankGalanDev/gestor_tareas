from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.templatetags.static import static
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import  CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.template import Context, loader 
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from backoffice.forms import MeetingForm
from backoffice.models import Meeting
from django.core.paginator import Paginator


class MeetingList(ListView):
    model = Meeting
    template_name = 'meetings/all_meetings.html'

    def get_queryset(self):
           
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Meeting.objects.filter(
                Q(nombre__icontains=search)| 
                Q(fecha__icontains=search)|
                Q(descripcion__icontains=search)|
                Q(objectives__icontains=search)|
                Q(start_time__icontains=search)|
                Q(members__email__icontains=search)|
                Q(members__name__icontains=search)|
                Q(members__first_name__icontains=search)|
                Q(members__last_name__icontains=search)|
                Q(members__rol__icontains=search)|
                Q(members__username__icontains=search)
               
                ).distinct()            
            
        else:
             Meeting.objects.all()
             

            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reuniones'
        context['table_title'] = 'Lista de reuniones'
        context['table_subtitle'] = 'Todas las reuniones'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MeetingDetail(DetailView):
    model = Meeting
    template_name = 'meetings/meeting_detail.html'
    success_url = reverse_lazy('all_meetings')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reuniones'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles de la reunion'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MeetingCreate(CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/new_meeting.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Reuniones'
        context['table_title'] = 'Nueva reunion'
        context['table_subtitle'] = 'Añada una reunion'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_meetings')



class MeetingUpdate(UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/meeting_update.html'
    success_url = reverse_lazy('all_meetings')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reuniones'
        context['table_title'] = 'Editar reunion'
        context['table_subtitle'] = 'Modificar reunion'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MeetingDelete(DeleteView):
    model = Meeting
    template_name = 'meetings/meeting_delete.html'
    success_url = reverse_lazy('all_meetings')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reuniones'
        context['table_title'] = 'Eliminar reunion'
        context['table_subtitle'] = 'Borre un reunion'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
