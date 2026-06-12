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
    identificador = models.CharField("identificador",unique=True, max_length=100, editable=False)
    estacion = models.IntegerField("Estacion de trabajo")
    is_active = models.BooleanField("Activo", default=True)
    descripcion = models.TextField("Descripcion",null=True, blank=True)
    date_reg = models.DateField("Fecha de ingreso", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.identificador:
            last_id = Equipo.objects.all().order_by('id').last()
            if not last_id:
                new_id_num = 1
            else:
                new_id_num = last_id.id + 1
            self.identificador = f"ccp{new_id_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dispositivo} - {self.identificador}  - {self.estacion} "

    
    class Meta:
        db_table = "equipo"
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

class Consumible(models.Model):
    name = models.CharField("Consumible", unique=True, max_length=100)
    cantidad = models.IntegerField("Cantidad", default=0)
    descripcion = models.TextField("Descripcion", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cantidad}"

    class Meta:
        db_table = "consumible"
        verbose_name = "Consumible"
        verbose_name_plural = "Consumibles"