from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from inventario.models import Equipo
from inventario.serializers import EquipoSerializer
from salapcs.models import SalaPC
from salapcs.serializers import SalaPCSerializer

from datetime import timedelta

from seguridad.decorators import logguer_required

class DashboardView(APIView):

    @logguer_required
    def get(self, request, format=None):
        
        hoy = timezone.localdate(timezone.now())
        lunes = hoy - timedelta(days=hoy.weekday())
        domingo = lunes + timedelta(days=6)
        print(f"Lunes: {lunes}, Domingo: {domingo}")
        equipos = Equipo.objects.all().count()
        salas = SalaPC.objects.filter(date__range=[lunes, domingo]).order_by('date', 'hour')

        sala_serializer = SalaPCSerializer(salas, many=True)

        data = {
            'user_id': request.user_id,
            'numero_equipos': equipos,
            'salas': sala_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)