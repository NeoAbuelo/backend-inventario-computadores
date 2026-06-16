from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from jose import jwt
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def generar_token(user):
    ahora = datetime.now(tz=timezone.utc)
    payload = {
        "user_id": user.id,
        "username": user.username,
        "iat": int(ahora.timestamp()),
        "exp": int((ahora + timedelta(days=settings.JWT_EXP_DAYS)).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def serializar_usuario(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
    }


class LoginView(APIView):
    """Inicio de sesión público. Devuelve un JWT y los datos del usuario."""

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        identificador = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")

        if not identificador or not password:
            return Response(
                {"status": "error", "message": "Usuario y contraseña son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Permite iniciar sesión con el correo además del nombre de usuario.
        username = identificador
        if "@" in identificador:
            user_obj = User.objects.filter(email=identificador).first()
            if user_obj:
                username = user_obj.username

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"status": "error", "message": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "status": "ok",
                "data": {"token": generar_token(user), "user": serializar_usuario(user)},
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    """Crea cuentas. Protegido: solo usuarios autenticados pueden registrar."""

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response(
                {"status": "error", "message": "Usuario y contraseña son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"status": "error", "message": "El usuario ya existe"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if email and User.objects.filter(email=email).exists():
            return Response(
                {"status": "error", "message": "El correo ya está registrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response(
            {
                "status": "ok",
                "message": "Usuario creado exitosamente",
                "data": serializar_usuario(user),
            },
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    """Devuelve los datos del usuario autenticado (validación de sesión)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response(
            {"status": "ok", "data": serializar_usuario(request.user)},
            status=status.HTTP_200_OK,
        )
