from django.apps import AppConfig


class BackofficeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backoffice'
'''
    def ready(self):
        from django.db.models.signals import post_save
        from backoffice.models import Task
        from backoffice.signals import actualizar_evolucion
        post_save.connect(actualizar_evolucion, sender=Task)

'''

    