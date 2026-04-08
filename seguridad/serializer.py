from rest_framework import serializers
from .models import Perfil 
from django.contrib.auth.models import User

class PerfilSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    mail = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Perfil
        fields = ['user', 'user_name', 'mail', 'cargo', 'permissions']