from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import LoginView, RegisterView, MeView

urlpatterns = [
    path("seguridad/login", LoginView.as_view(), name="login"),
    path("seguridad/register", RegisterView.as_view(), name="register"),
    path("seguridad/me", MeView.as_view(), name="me"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
