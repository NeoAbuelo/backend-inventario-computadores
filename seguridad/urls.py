from django.urls import path
from .views import CreateUserView, LogginView , PerfilView

urlpatterns = [
    path('seguridad/reg', CreateUserView.as_view(), name='register'),
    path('seguridad/login', LogginView.as_view(), name='login'),
    path('seguridad/perfil/<int:id>', PerfilView.as_view(), name='perfil'),
]