
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, JsonResponse
from django.db.models import Avg
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.templatetags.static import static
from django.views import View
from django.views.generic import  ListView, DetailView, View
from django.views.generic.edit import  CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.template import Context, loader 
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy

from accounts.models import CustomUser
from django.core.paginator import Paginator

from backoffice.models import Membership, Meeting, Team
from backoffice.forms import MembershipForm
 

from backoffice.forms import TeamForm, MembershipFormSet







#CRUD
class MembershipList(LoginRequiredMixin,  ListView):
    model = Membership
    paginate_by = 20
    template_name = 'members/all_members.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Membership.objects.filter(
                Q(team__team_name__icontains=search)| 
                Q(user__username__icontains=search)|
                Q(user__name__icontains=search)|
                Q(user__lastname__icontains=search)|
                Q(user__firstname__icontains=search)|
                Q(user__rol__icontains=search)|
                Q(meeting__meeting_name__icontains=search)
               
               
              
              
                ).distinct()            
            
        else:
            Membership.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Equipos'
        context['table_title'] = 'Lista de equipos'
        context['table_subtitle'] = 'Todos los equipos'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MembershipCreate(LoginRequiredMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'members/new_member.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Equipos'
        context['table_title'] = 'Nuevo equipo'
        context['table_subtitle'] = 'Añada un equipo'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_members')



class MembershipDetail(LoginRequiredMixin, DetailView):
    model = Membership
    template_name = 'members/detail_member.html'
    success_url = reverse_lazy('all_members')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles del equipo'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MembershipUpdate(LoginRequiredMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    template_name = 'members/update_member.html'
    success_url = reverse_lazy('all_members')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['table_title'] = 'Editar equipo'
        context['table_subtitle'] = 'Modificar equipo'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class MembershipDelete(LoginRequiredMixin, DeleteView):
    model = Membership
    template_name = 'members/delete_member.html'
    success_url = reverse_lazy('all_members')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['table_title'] = 'Eliminar equipo'
        context['table_subtitle'] = 'Borre un equipo'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


'''

class AddUserToGroupView(View):
    template_name = 'members/add_user_to_member.html'
    



    def get(self, request, pk):
            group = get_object_or_404(Group, pk=pk)
            form = AddUsersToGroupForm(group.id)
            return render(request, self.template_name, {'form': form, 'group': group})

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        form = AddUsersToGroupForm(group.id, request.POST)
        if form.is_valid():
            users = form.cleaned_data['users']
            group.user_set.add(*users)
            return redirect('all_members')
        return render(request, self.template_name, {'form': form, 'group': group})




class RemoveUserFromGroupView(LoginRequiredMixin, CreateView):
    model = CustomUser
    template_name = 'members/remove_user_from_member.html'
    form_class = RemoveUserFromGroupForm
    success_url = reverse_lazy('all_members')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Group.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        group = form.cleaned_data['group']
        users = form.cleaned_data['users']
        group.user_set.remove(*users)
        return super().form_valid(form)

'''

