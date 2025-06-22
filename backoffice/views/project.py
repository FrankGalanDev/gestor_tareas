
from django.shortcuts import render, get_object_or_404, redirect

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
from backoffice.forms import ProjectForm
from backoffice.models import Project, Supercolumn,Column,Task
from accounts.models import CustomUser
from django.core.paginator import Paginator



#CRUD
class ProjectList(LoginRequiredMixin,  ListView):
    model = Project
    paginate_by = 20
    template_name = 'projects/all_projects.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Project.objects.filter(
                Q(project_name__icontains=search)| 
                Q(project_description__icontains=search)|
                Q(supercolumn__supercolumn_name__icontains=search)| 
                Q(task__task_name__icontains=search)
               
              
                ).distinct()            
            
        else:
             Project.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Proyectos'
        context['table_title'] = 'Lista de proyectos'
        context['table_subtitle'] = 'Todos los proyectos'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/new_project.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Proyectos'
        context['table_title'] = 'Nuevo proyecto'
        context['table_subtitle'] = 'Añada un proyecto'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_projects')



class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/detail_project.html'
    success_url = reverse_lazy('all_projects')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        context['title'] = 'Proyectos'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles del proyecto'
        context['super'] = Supercolumn.objects.filter(project=project)
        context['columnas'] = Column.objects.filter(superior__project=project)
        context['tareas'] = Task.objects.filter(project=project)
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/update_project.html'
    success_url = reverse_lazy('all_projects')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyectos'
        context['table_title'] = 'Editar proyecto'
        context['table_subtitle'] = 'Modificar proyecto'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/delete_project.html'
    success_url = reverse_lazy('all_projects')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Proyectos'
        context['table_title'] = 'Eliminar proyecto'
        context['table_subtitle'] = 'Borre un proyecto'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 