
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
from backoffice.forms import ColumnForm
from backoffice.models import Column
from accounts.models import CustomUser
from django.core.paginator import Paginator



#CRUD
class ColumnList(LoginRequiredMixin,  ListView):
    model = Column
    paginate_by = 20
    template_name = 'columns/all_columns.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Column.objects.filter(
                Q(column_name__icontains=search)| 
                Q(column_description__icontains=search)
              
                ).distinct()            
            
        else:
             Column.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Columnas'
        context['table_title'] = 'Lista de columnas'
        context['table_subtitle'] = 'Todas las columnas'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ColumnCreate(LoginRequiredMixin, CreateView):
    model = Column
    form_class = ColumnForm
    template_name = 'columns/new_column.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Columnas'
        context['table_title'] = 'Nueva columna'
        context['table_subtitle'] = 'Añada una columna'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_columns')



class ColumnDetail(LoginRequiredMixin, DetailView):
    model = Column
    template_name = 'columns/detail_column.html'
    success_url = reverse_lazy('all_columns')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'columnas'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles de la columna'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ColumnUpdate(LoginRequiredMixin, UpdateView):
    model = Column
    form_class = ColumnForm
    template_name = 'columns/update_column.html'
    success_url = reverse_lazy('all_columns')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'columnas'
        context['table_title'] = 'Editar columna'
        context['table_subtitle'] = 'Modificar columna'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class ColumnDelete(LoginRequiredMixin, DeleteView):
    model = Column
    template_name = 'columns/delete_column.html'
    success_url = reverse_lazy('all_columns')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'columnas'
        context['table_title'] = 'Eliminar columna'
        context['table_subtitle'] = 'Borre un columna'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


