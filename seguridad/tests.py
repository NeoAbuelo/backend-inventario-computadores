from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin", email="admin@test.cl", password="clave-segura-123"
        )

    def test_login_ok_devuelve_token(self):
        res = self.client.post(
            "/api/v1/seguridad/login",
            {"username": "admin", "password": "clave-segura-123"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data["data"])

    def test_login_credenciales_invalidas(self):
        res = self.client.post(
            "/api/v1/seguridad/login",
            {"username": "admin", "password": "mala"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ruta_protegida_sin_token_401(self):
        res = self.client.get("/api/v1/equipos")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ruta_protegida_con_token_ok(self):
        token = self.client.post(
            "/api/v1/seguridad/login",
            {"username": "admin", "password": "clave-segura-123"},
            format="json",
        ).data["data"]["token"]
        res = self.client.get(
            "/api/v1/equipos", HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crear_reserva_es_publico(self):
        res = self.client.get("/api/v1/salapcs")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_listar_profesores_es_publico(self):
        res = self.client.get("/api/v1/profesores")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crear_profesor_requiere_login(self):
        res = self.client.post(
            "/api/v1/profesores",
            {"correo": "x@x.cl", "asignatura": "Mate"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
