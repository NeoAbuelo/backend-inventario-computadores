from rest_framework import serializers
from .models import Profesor, SalaPC

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ["id", "nombre", "apellido", "correo", "asignatura"]

class SalaPCSerializer(serializers.ModelSerializer):
    profesor_name = serializers.ReadOnlyField(source='profesor.nombre')
    class Meta:
        model = SalaPC
        fields = ["id", "profesor", "profesor_name", "curso", "asignatura", "date", "hour"]