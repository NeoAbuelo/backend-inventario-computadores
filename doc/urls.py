from django.urls import path
from . import views

app_name = 'doc'

urlpatterns = [
    path('', views.index, name='index'),
    path('inventario/', views.inventario, name='inventario'),
    path('salapcs/', views.salapcs, name='salapcs'),
]
