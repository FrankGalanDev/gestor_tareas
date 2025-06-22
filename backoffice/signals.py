# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from backoffice.models import Task   # Importamos la clase Task desde models.py
from datetime import datetime   # También importamos datetime para obtener la fecha actual


'''
@receiver(post_save, sender=Task)

    def actualizar_evolucion(sender, instance, **kwargs):
        instance.pool_evolucion += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Progreso {str(instance.progreso)}%\n"
        instance.save()
    
#Para solucionar el error "maximum recursion depth exceeded while calling a Python object" en la función save(), 
# se puede implementar un contador para limitar la profundidad de la recursión.
# En lugar de llamar directamente a instance.save(), se puede crear una variable llamada "counter" 
# para contar el número de veces que la función ha sido llamada. Si el contador alcanza un límite predefinido, 
# la función save() simplemente regresará sin realizar ninguna operación adicional. Esto previene la profundidad 
# excesiva de la recursión. En este caso 49

@receiver(post_save, sender=Task)
def actualizar_evolucion(sender, instance, **kwargs):
    instance.pool_evolucion += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Progreso {str(instance.progreso)}%\n"
    counter = getattr(instance, '_save_counter', 0) + 1
    if counter > 2:
        return
    setattr(instance, '_save_counter', counter)
    instance.save()'''