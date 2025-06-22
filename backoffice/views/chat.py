from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.views.generic import  ListView,DetailView
from django.views.generic.edit import  CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_protect
from django.template import Context, loader 
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

#from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from backoffice.forms import ChatForm, ResponseChatForm
from backoffice.models import Chat
from accounts.models import CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden


# Create your views here.

class ChatList( LoginRequiredMixin, ListView):
    
    model = Chat
    paginate_by = 20
    template_name = 'chats/all_chats.html'

    #queryset para filtro
    def get_queryset(self):   
        search= self.request.GET.get('busqueda')
        if search:
            
            return Chat.objects.filter(
                Q(message_topic__icontains=search)|
                Q(message_reference__icontains=search)|
                Q(sender__name__icontains=search)| 
                Q(sender__first_name__icontains=search)|
                Q(sender__last_name__icontains=search)|
                Q(sender__username__icontains=search)|
                Q(receiver__name__icontains=search)| 
                Q(receiver__first_name__icontains=search)|
                Q(receiver__last_name__icontains=search)|
                Q(receiver__username__icontains=search)|
                Q(message_text__icontains=search)            
                ).distinct()
            
            
        else:
            Chat.objects.all()
            
        return super().get_queryset()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mensajes'
        context['table_title'] = 'Lista de mensajes'
        context['table_subtitle'] = 'Todos los mensajes'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ChatCreate(LoginRequiredMixin,CreateView):
    
    model = Chat
    form_class = ChatForm
    template_name = 'chats/new_chat.html' 

    #Introducing automatically the especific value in the field sender, it's take the current user id 
    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mensajes'
        context['table_title'] = 'Nuevo mensaje'
        context['table_subtitle'] = 'Añada un mensaje'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_chats')


class ChatUpdate( LoginRequiredMixin, UpdateView):
    
    model = Chat
    form_class = ChatForm
    template_name = 'chats/update_chat.html'
    success_url = reverse_lazy('all_chats')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mensajes'
        context['table_title'] = 'Editar mensaje'
        context['table_subtitle'] = 'Modificar mensaje'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ChatDetail( LoginRequiredMixin, DetailView):
   
    model= Chat
    template_name='chats/see_message.html'

    #Introducing automatically the especific value in the field sender, it's take the current user id 
    def form_valid(self, form):
        form.instance.message_reference = self.id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResponseChatForm
        context['title'] = 'Mensaje'
        context['Response'] = 'Responder mensaje'
        
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@permission_required ('backoffice.add_chat', raise_exception=True)
def message_response(request,message_id):
    
    anterior = Chat.objects.get(id=message_id)
    responses = Chat.objects.all().filter(message_reference=anterior)
    if anterior:
        anterior.status = 'leido'
        anterior.save()
        #return redirect('message_response', pk=message_id)
        
    
    if request.method == 'POST':
        
        form = ResponseChatForm(request.POST)    
        
        if form.is_valid():
            new_form=form.save(commit=False) 
            new_form.message_reference = anterior
            new_form.sender = request.user
            
            new_form.save()
            return redirect('all_chats')
                        
    else:
        form = ResponseChatForm()

    context={
        'anterior':anterior,
        'form':form,
        'responses':responses
    }

    return render(request,'chats/message_response.html',context)


@permission_required ('backoffice.view_chat', raise_exception=True)
def message_thread(request, message_id):

    original = Chat.objects.get(pk=message_id)
    hilo= Chat.objects.all().filter(message_reference=original)
    cantidad = hilo.count()
    form = ResponseChatForm
   
    if request.method=='POST':
        form = ResponseChatForm(request.POST) 
        if form.is_valid():
            new_form=form.save(commit=False) 
            new_form.message_reference = original
            new_form.sender = request.user
            #new_form.message_topic =original.message_topic
                
            new_form.save()
            #return redirect('message_response', pk=message_id)

    context ={
        'original': original,
        'hilo':hilo,
        'cantidad':cantidad,
        'form':form
    }
    return render(request, 'chats/message_thread.html', context)



class ChatDelete(LoginRequiredMixin, DeleteView):
    model = Chat
    template_name = 'chats/delete_message.html'
    success_url = reverse_lazy('all_messages')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mensajes'
        context['table_title'] = 'Eliminar mensaje'
        context['table_subtitle'] = 'Borre un mensaje'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

