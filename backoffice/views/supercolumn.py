
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
from backoffice.forms import SupercolumnForm
from backoffice.models import Supercolumn
from django.core.paginator import Paginator



#CRUD
class SupercolumnList(LoginRequiredMixin,  ListView):
    model = Supercolumn
    paginate_by = 20
    template_name = 'supercolumns/all_supercolumns.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Supercolumn.objects.filter(
                Q(supercolumn_name__icontains=search)| 
                Q(supercolumn_description__icontains=search)
              
                ).distinct()            
            
        else:
             Supercolumn.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Supercolumnas'
        context['table_title'] = 'Lista de supercolumnas'
        context['table_subtitle'] = 'Todas las supercolumnas'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class SupercolumnCreate(LoginRequiredMixin, CreateView):
    model = Supercolumn
    form_class = SupercolumnForm
    template_name = 'supercolumns/new_supercolumn.html' 

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
        return reverse('all_supercolumns')



class SupercolumnDetail(LoginRequiredMixin, DetailView):
    model = Supercolumn
    template_name = 'supercolumns/detail_column.html'
    success_url = reverse_lazy('all_supercolumns')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Supercolumnas'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles de la supercolumna'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class SupercolumnUpdate(LoginRequiredMixin, UpdateView):
    model = Supercolumn
    form_class = SupercolumnForm
    template_name = 'supercolumns/update_supercolumn.html'
    success_url = reverse_lazy('all_supercolumns')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Supercolumnas'
        context['table_title'] = 'Editar supercolumna'
        context['table_subtitle'] = 'Modificar supercolumna'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class SupercolumnDelete(LoginRequiredMixin, DeleteView):
    model = Supercolumn
    template_name = 'supercolumns/delete_supercolumn.html'
    success_url = reverse_lazy('all_supercolumns')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Supercolumnas'
        context['table_title'] = 'Eliminar supercolumna'
        context['table_subtitle'] = 'Borre un supercolumna'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


