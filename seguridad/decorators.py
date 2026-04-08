from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from jose import jwt
from django.conf import settings
import time

def logguer_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header==None:
            return Response({'error': 'Token de autenticación es requerido'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS512'])
            
            if payload['exp'] < time.time():
                return Response({'error': 'Token ha expirado'}, status=status.HTTP_401_UNAUTHORIZED)
            request.user_id = payload['user_id']

        except (jwt.JWTError, IndexError):
            return Response({'error': 'Token de autenticación inválido'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header==None:
            return Response({'error': 'Token de autenticación es requerido'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS512'])
            
            if payload['exp'] < time.time():
                return Response({'error': 'Token ha expirado'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if payload['role'] != 'admin':
                return Response({'error': 'Permisos insuficientes'}, status=status.HTTP_403_FORBIDDEN)

            request.user_id = payload['user_id']

        except (jwt.JWTError, IndexError):
            return Response({'error': 'Token de autenticación inválido'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper