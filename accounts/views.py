from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from accounts.forms import CustomUserForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from django.http import HttpResponse, JsonResponse
from django.utils.decorators  import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect


'''
#HOME
@login_required
def home(request):
    return render(request, 'home.html')

class UserList(ListView):
    template_name = CustomUser
    template_name = 'all_usuarios.html'

#SIGNUP
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'account_activation_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})





Primero, importamos las librerías necesarias.
Definimos la función activate que recibe request, uidb64 y token como parámetros.
Luego, tratamos de decodificar el valor de uidb64 y obtenemos el usuario correspondiente.
Si el usuario es válido y el token es correcto, activamos la cuenta del usuario y redirigimos a la página de inicio de sesión.
Si no, mostramos un mensaje de error y redirigimos a la página de registro.




#ACCOUNT ACTVATE
@login_required
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido activada exitosamente.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de activación es inválido o ha expirado.')
        return redirect('register')



#REGISTER
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Welcome to our Kanban System!'
            message = f'Dear {user.username},\n\nThank you for registering to our Kanban System!\n\nBest regards,\nThe Kanban Team'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list, fail_silently=True)
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


#LOGIN

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login/login.html')


#LOGOUT
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


#CHANGE PASSWORD
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed!')
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

'''





#BASED CLASS CRUD  FOR CUSTOM DASHBOARD
class CustomUserList(LoginRequiredMixin,  ListView):
    model = CustomUser
    paginate_by = 20
    template_name = 'users/all_users.html'


    def get_queryset(self):
       
        search= self.request.GET.get('busqueda')
        if search:
            #hostname__startswith = self.request.GET['acronym']
            
            return CustomUser.objects.filter(
                Q(username__icontains=search)|
                Q(rol__icontains=search)|
                Q(name__icontains=search)|
                Q(first_name__icontains = search)|
                Q(last_name__icontains= search)|
                Q(username__icontains= search)|
                Q(phone__icontains= search)| 
                Q(email__icontains= search)
                ).distinct()         
            
        else:
             CustomUser.objects.all()
            
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Usuarios'
        context['table_title'] = 'Lista de usuarios'
        context['table_subtitle'] = 'Todas los usuarios'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class CustomUserCreate(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'users/new_user.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Usuarios'
        context['table_title'] = 'Nuevo usuario'
        context['table_subtitle'] = 'Añada un  usuario'
        context['action'] ='add'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('all_users')



class CustomUserDetail(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/detail_user.html'
    success_url = reverse_lazy('all_users')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['table_title'] = 'Especificaciones'
        context['table_subtitle'] = 'Detalles del usuario'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class CustomUserUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('all_users')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['table_title'] = 'Editar usuario'
        context['table_subtitle'] = 'Modificar usuario'
        context['action'] ='edit'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class CustomUserDelete(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('all_users')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        context['table_title'] = 'Eliminar usuario'
        context['table_subtitle'] = 'Borre un usuario'
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


