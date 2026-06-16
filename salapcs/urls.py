from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.profesor_views import ProfesorList, ProfesorDetail
from .views.salapcs_views import SalaPCList, SalaPCDetail
from .views.reporteshorario import ReporteHorarioView

urlpatterns = [
    path("profesores",ProfesorList.as_view(),name="list-profesores"),
    path("profesores/<int:pk>",ProfesorDetail.as_view(),name="detail-profesor"),
    path("salapcs",SalaPCList.as_view(),name="list-salapcs"),
    path("salapcs/<int:pk>",SalaPCDetail.as_view(),name="detail-salapc"),
    path("salapcs/reportes/horario", ReporteHorarioView.as_view(), name="reporte-horario")
]

urlpatterns = format_suffix_patterns(urlpatterns)
