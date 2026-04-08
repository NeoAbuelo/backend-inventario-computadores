from django.db import models

# Create your models here.
class Dispositivo(models.Model):
    name = models.CharField("Dispositivo", unique=True, max_length=100)
    descripcion = models.TextField("Descripcion", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dispositivo"
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

class Equipo(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    marca = models.CharField("Marca", blank=True, null=True, max_length=100)
    modelo = models.CharField("Modelo",blank=True,null=True, max_length=100)
    identificador = models.CharField("identificador",unique=True, max_length=100)
    estacion = models.IntegerField("Estacion de trabajo",unique=True)
    is_active = models.BooleanField("Activo", default=True)
    descripcion = models.TextField("Descripcion",null=True, blank=True)
    date_reg = models.DateField("Fecha de ingreso")

    def __str__(self):
        return f"{self.dispositivo} - {self.identificador}  - {self.estacion} "

    class Meta:
        db_table = "equipo"
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

