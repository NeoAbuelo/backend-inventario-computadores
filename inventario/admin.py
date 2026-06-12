from django.contrib import admin
from .models import Dispositivo,  Equipo, Consumible

# Register your models here.
admin.site.register(Dispositivo)
admin.site.register(Equipo)
admin.site.register(Consumible)
