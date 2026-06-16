from django.conf import settings
from django.contrib.auth.models import User
from jose import jwt, JWTError
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    """Autenticación por JWT (python-jose) integrada con DRF.

    Lee el encabezado ``Authorization: Bearer <token>``, valida la firma y la
    expiración (jose lanza ``JWTError`` si el token expiró) y deja el ``User``
    correspondiente en ``request.user`` para que ``IsAuthenticated`` funcione.

    Devuelve ``None`` cuando no hay encabezado, de modo que la capa de permisos
    decide (con ``IsAuthenticated`` esto resulta en 401).
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            raise exceptions.AuthenticationFailed("Encabezado de autorización inválido")

        token = parts[1]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except JWTError:
            raise exceptions.AuthenticationFailed("Token inválido o expirado")

        try:
            user = User.objects.get(id=payload.get("user_id"), is_active=True)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Usuario no encontrado")

        return (user, token)

    def authenticate_header(self, request):
        # Hace que las respuestas 401 incluyan el encabezado WWW-Authenticate.
        return self.keyword
