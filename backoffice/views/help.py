from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import  CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.template import Context, loader 
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


#from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from backoffice.forms import HelpForm
from backoffice.models import Help
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden


# Create your views here.

class HelpList( LoginRequiredMixin,  ListView):
    model = Help
    paginate_by = 12
    template_name = 'helps/help.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:           
            
            return Help.objects.filter(
                Q(title__icontains=search)| 
                Q(subtitle__icontains=search)|
                Q(description__icontains=search)
                
                                ).distinct()
            
            
        else:
             Help.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ayuda'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class HelpCreate( LoginRequiredMixin, CreateView):
    model = Help
    form_class = HelpForm
    template_name = 'helps/help_create.html' 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Ayuda'
        context['table_title'] = 'Nueva ayuda'
        context['table_subtitle'] = 'Añada una ayuda'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('help')



class HelpDetail( LoginRequiredMixin, DetailView):    
    model = Help
    template_name = 'helps/help_detail.html'
    success_url = reverse_lazy('help')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ayuda'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles de la ayuda'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class HelpUpdate(LoginRequiredMixin, UpdateView):    
    model = Help
    form_class = HelpForm
    template_name = 'helps/help_update.html'
    success_url = reverse_lazy('help')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ayuda'
        context['table_title'] = 'Editar ayuda'
        context['table_subtitle'] = 'Modificar ayuda'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class HelpDelete( LoginRequiredMixin, DeleteView):
    
    model = Help
    template_name = 'helps/help_delete.html'
    success_url = reverse_lazy('help')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ayuda'
        context['table_title'] = 'Eliminar ayuda'
        context['table_subtitle'] = 'Borre un ayuda'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)