from rest_framework import serializers
from .models import Profesor, SalaPC

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ["nombre", "apellido", "correo", "asignatura"]

class SalaPCSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer()
    class Meta:
        model = SalaPC
        fields = ["profesor", "curso", "asignatura", "date", "hour"]