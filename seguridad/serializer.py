from rest_framework import serializers
from .models import Perfil 
from django.contrib.auth.models import User

class PerfilSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    mail = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Perfil
        fields = ['user', 'mail', 'cargo']