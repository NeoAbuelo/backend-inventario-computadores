from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Consumible


class ReporteConsumiblesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="clave-123")
        Consumible.objects.create(name="Toner", cantidad=2, descripcion="Bajo stock")
        Consumible.objects.create(name="Resma", cantidad=10)

    def _token(self):
        return self.client.post(
            "/api/v1/seguridad/login",
            {"username": "admin", "password": "clave-123"},
            format="json",
        ).data["data"]["token"]

    def test_pdf_requiere_login(self):
        res = self.client.get("/api/v1/consumibles/pdf")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pdf_autenticado_devuelve_pdf(self):
        res = self.client.get(
            "/api/v1/consumibles/pdf",
            HTTP_AUTHORIZATION=f"Bearer {self._token()}",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res["Content-Type"], "application/pdf")
