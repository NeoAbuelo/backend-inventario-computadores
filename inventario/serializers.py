from rest_framework import serializers
from .models import Dispositivo, Equipo, Consumible

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = ['id', 'name', 'descripcion']

class EquipoSerializer(serializers.ModelSerializer):
    dispositivo_name = serializers.ReadOnlyField(source= 'dispositivo.name')
    class Meta:
        model = Equipo
        fields = ['id', 'dispositivo' ,'dispositivo_name', 'marca', 'modelo', 'identificador', 'estacion', 'descripcion', 'date_reg', 'is_active']
        read_only_fields = ['identificador', 'date_reg']

class ConsumibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumible
        fields = ['id', 'name', 'cantidad', 'descripcion']