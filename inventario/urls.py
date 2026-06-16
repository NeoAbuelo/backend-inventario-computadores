from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.dispositivos_views import DispositivoList, DispositivoDetail
from .views.equipos_views import EquipoListCreateView, EquipoDetailView, EquipoListByDispositivoView
from .views.cosumibles_views import ConsumibleList, ConsumibleDetail
from .views.reportesequipos import ReporteEquiposView
from .views.reportesconsumibles import ReporteConsumiblesView

urlpatterns = [
    path("dispositivos",DispositivoList.as_view(),name="list-dispositivos"),
    path("dispositivos/<int:pk>",DispositivoDetail.as_view(),name="detail-dispositivo"),
    path("equipos",EquipoListCreateView.as_view(),name="list-equipos"),
    path("equipos/pdf",ReporteEquiposView.as_view(),name="reporte-equipos"),
    path("equipos/<int:pk>",EquipoDetailView.as_view(),name="detail-equipo"),
    path("equipos/dispositivo/<int:dispositivo_id>",EquipoListByDispositivoView.as_view(),name="list-equipos-by-dispositivo"),
    path("consumibles",ConsumibleList.as_view(),name="list-consumibles"),
    path("consumibles/pdf",ReporteConsumiblesView.as_view(),name="reporte-consumibles"),
    path("consumibles/<int:pk>",ConsumibleDetail.as_view(),name="detail-consumible"),
]

urlpatterns = format_suffix_patterns(urlpatterns)