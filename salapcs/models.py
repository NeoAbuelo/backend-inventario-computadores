from django.db import models

# Create your models here.
class Profesor(models.Model):
    nombre = models.CharField("Nombre", max_length=100, blank=True, null=True )
    apellido = models.CharField("Apellido", max_length=100, blank=True, null=True)
    correo = models.EmailField("Correo")
    asignatura = models.CharField("Asignatura", max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.correo} | {self.asignatura}"
    
    class Meta:
        db_table = "profesor"
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

class SalaPC(models.Model):
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    curso = models.CharField("Curso", max_length=100)
    asignatura = models.CharField("Asignatura", max_length=100)
    date = models.DateField("Fecha de uso")
    hour = models.TimeField("Hora de inicio")

    def __str__(self):
        return f"{self.profesor} - {self.curso}: dia {self.date} a las {self.hour}"

    class Meta:
        db_table = "salapc"
        verbose_name = "SalaPC"
        verbose_name_plural = "SalasPC"