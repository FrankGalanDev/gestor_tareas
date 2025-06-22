from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_TYPE=(
    ('analista de datos' , 'analista de datos'),
    ('jefe de area' , 'jefe de area'),
    ('especialista' , 'especialista')
)


class CustomUser(AbstractUser):
    #foreing key
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    username = models.CharField('Apodo o Nick:', max_length=100,  unique=True, blank= True, null=True)
    name =models.CharField('Nombre de usuario:', max_length=100, blank= True, null=True)
    first_name= models.CharField('Primer Apellido:', max_length=100, blank= True, null=True) 
    last_name = models.CharField('Segundo Apellido:', max_length=100, blank= True, null=True)
    is_staff= models.BooleanField('Empleado:',default=False)
    is_active = models.BooleanField(
        default=True, help_text="Miembro activo:")
    phone = models.CharField('Teléfono', max_length=12, blank=True, null=True,  unique= True)
    photo=  models.ImageField(
        upload_to='static/avatars',
        blank = True,
        null = True
    )
    
    on = models.BooleanField('Activar',default='1') #borrar luego se repite con is_active
    rol = models.CharField('Rol',
        choices=ROLE_TYPE, 
        max_length=31, 
        blank=True, 
        null=True, 
        default='analista de datos')

    
        
    class Meta:
        ordering = ['username']
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('all_users.html', kwargs={'pk':self.id})   



