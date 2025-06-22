
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
from backoffice.models import Team, Meeting
from django.core.paginator import Paginator
#from django.contrib.auth.models import Group
from backoffice.forms import TeamForm, MembershipFormSet








#CRUD
class TeamList(LoginRequiredMixin,  ListView):
    model = Team
    paginate_by = 20
    template_name = 'teams/all_teams.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return Team.objects.filter(
                Q(team_name__icontains=search)| 
                Q(member__username__icontains=search)|
                Q(member__name__icontains=search)|
                Q(member__lastname__icontains=search)|
                Q(member__firstname__icontains=search)|
                Q(member__rol__icontains=search)
               
               
              
              
                ).distinct()            
            
        else:
            Team.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Equipos'
        context['table_title'] = 'Lista de equipos'
        context['table_subtitle'] = 'Todos los equipos'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/new_team.html' 
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Equipos'
        context['table_title'] = 'Nuevo equipo'
        context['table_subtitle'] = 'Añada un equipo'
        context['action'] ='add'
        return context

    '''

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['users'] = CustomUser.objects.all()
        data['page_title'] = 'Equipos'
        data['table_title'] = 'Nuevo equipo'
        data['table_subtitle'] = 'Añada un equipo'
        data['action'] ='add'
        if self.request.POST:
            data['memberships'] = MembershipFormSet(self.request.POST)
        else:
            data['memberships'] = MembershipFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        memberships = context['memberships']
        if memberships.is_valid():
            self.object = form.save()
            memberships.instance = self.object
            memberships.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, memberships=memberships))



    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_teams')




class TeamDetail(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/detail_team.html'
    success_url = reverse_lazy('all_teams')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles del equipo'
        

        return context






class TeamUpdate(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/update_team.html'
    success_url = reverse_lazy('all_teams')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['table_title'] = 'Editar equipo'
        context['table_subtitle'] = 'Modificar equipo'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    template_name = 'teams/delete_team.html'
    success_url = reverse_lazy('all_teams')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Equipos'
        context['table_title'] = 'Eliminar equipo'
        context['table_subtitle'] = 'Borre un equipo'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



'''
class AddUserToGroupView(CreateView):
    model = CustomUser
    template_name = 'teams/add_user_to_group.html'
    form_class = AddUserTeamForm
    success_url = reverse_lazy('all_teams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.get(pk=self.kwargs['pk'])
        context['title'] = 'Equipos'
        context['table_title'] = 'Añadir miembros al equipo'
        context['table_subtitle'] = 'Configuración'
        return context

    def form_valid(self, form):
        group = Group.objects.get(pk=self.kwargs['pk'])
        user = form.save()
        group.user_set.add(user)
        return super().form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)





class AddUserToGroupView(View):
    template_name = 'teams/add_user_to_team.html'
    



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
            return redirect('all_teams')
        return render(request, self.template_name, {'form': form, 'group': group})




class RemoveUserFromGroupView(LoginRequiredMixin, CreateView):
    model = CustomUser
    template_name = 'teams/remove_user_from_team.html'
    form_class = RemoveUserFromGroupForm
    success_url = reverse_lazy('all_teams')

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


def meetings_chart(request, team_id):
    team = Team.objects.get(id=team_id)
    meetings = Meeting.objects.filter(team=team)
    meetings_data = meetings[0].meetings_per_month()
    months = [m[0] for m in meetings_data]
    counts = [m[1] for m in meetings_data]
    context = {
    'team': team,
    'months': months,
    'counts': counts,
    }
    return render(request, 'teams/meetings_chart.html', context)