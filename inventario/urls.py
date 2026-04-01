from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.dispositivos_views import DispositivoList, DispositivoDetail
from .views.equipos_views import EquipoListCreateView, EquipoDetailView, EquipoListByDispositivoView


urlpatterns = [
    path("dispositivos",DispositivoList.as_view(),name="list-dispositivos"),
    path("dispositivos/<int:pk>",DispositivoDetail.as_view(),name="detail-dispositivo"),
    path("equipos",EquipoListCreateView.as_view(),name="list-equipos"),
    path("equipos/<int:pk>",EquipoDetailView.as_view(),name="detail-equipo"),
    path("equipos/dispositivo/<int:dispositivo_id>",EquipoListByDispositivoView.as_view(),name="list-equipos-by-dispositivo")

]

urlpatterns = format_suffix_patterns(urlpatterns)