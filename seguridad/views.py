from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings

from django.db import transaction
from jose import jwt
import os 
import uuid
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv
from django.contrib.auth.models import User
from .models import Perfil
from .serializer import PerfilSerializer

from .decorators import logguer_required

load_dotenv()

# Create your views here.
class CreateUserView(APIView):

    def post(self, request, format=None):
        if request.data.get('username')==None or not request.data.get('username'):
            return Response({'error': 'nombre de usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST) 
        if request.data.get('password')==None or not request.data.get('password'):
            return Response({'error': 'contraseña es requerida'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('email')==None or not request.data.get('email'):
            return Response({'error': 'correo electrónico es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'correo electrónico ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=request.data.get('username'),
                    email=request.data.get('email'),
                    password=request.data.get('password')
                )
                perfil = Perfil.objects.create(
                    user=user,
                    cargo=request.data.get('cargo', 'Profesor'),
                    permissions = 'profesor'
                )
                
                return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'Error inesperado'}, status=status.HTTP_400_BAD_REQUEST)
        
class LogginView(APIView):

    def post(self, request, format=None):
        if request.data.get('email')==None or not request.data.get('email'):
            return Response({'error': 'correo electrónico es requerido'}, status=status.HTTP_400_BAD_REQUEST) 
        if request.data.get('password')==None or not request.data.get('password'):
            return Response({'error': 'contraseña es requerida'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(request, username=user.username, password=request.data.get('password'))
        if user is not None:
            fecha = datetime.now()
            despues = fecha + timedelta(days=1)
            feche_unix = int(datetime.timestamp(despues))
            payload = {
                'user_id': user.id,
                'ISS': os.getenv('BASE_URL'),
                'iat': int(time.time()),
                'exp': feche_unix,
                'role': user.perfil.permissions
            }
            try:
                token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS512')
                return Response({
                        'id': user.id, 
                        'username': user.username, 
                        'token': token,
                        'role': user.perfil.permissions}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Error al generar el token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        

class PerfilView(APIView):

    @logguer_required
    def get(self, request, format=None):
        try:
            perfil = Perfil.objects.get(user=request.user_id)
            serializer = PerfilSerializer(perfil)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Perfil.DoesNotExist:
            return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)