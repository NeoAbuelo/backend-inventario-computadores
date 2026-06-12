from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField("Cargo", max_length=255, blank=True)
    permissions = models.CharField("Permissions", max_length=255, choices=[('admin', 'Admin'), ('profesor', 'Profesor')])
    
    def __str__(self):
        return self.user.username
