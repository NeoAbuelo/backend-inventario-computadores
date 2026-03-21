from rest_framework import serializers
from .models import Dispositivo, Equipo

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = ['id', 'name', 'descripcion']


class EquipoSerializer(serializers.ModelSerializer):
    dispositivo = serializers.ReadOnlyField(source= 'dispositivo.name')
    class Meta:
        model = Equipo
        fields = ['id', 'dispositivo' ,'marca', 'modelo', 'identificador', 'estacion', 'descripcion', 'date_reg']
