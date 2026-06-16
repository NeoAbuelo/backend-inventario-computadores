from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.http import Http404

from ..models import SalaPC
from ..serializers import SalaPCSerializer
from .paginatios import CustomPagination


class SalaPCList(APIView):
    # Público: cualquiera puede consultar y agendar horas de la sala
    # (formulario público de agendamiento). La edición/borrado de reservas
    # (SalaPCDetail) sí requiere autenticación.
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        salapcs = SalaPC.objects.all().order_by('-date', '-hour')
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(salapcs, request)
        serializer = SalaPCSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        date = request.data.get("date")
        hour = request.data.get("hour")
        if date and hour and SalaPC.objects.filter(date=date, hour=hour).exists():
            return Response(
                {"status": "error", "message": "Ya existe una reserva para esa fecha y hora. Elige otro horario."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = SalaPCSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "Reserva de sala creada exitosamente"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Error al crear la SalaPC", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SalaPCDetail(APIView):
    def get_object(self, pk):
        try:
            return SalaPC.objects.get(pk=pk)
        except SalaPC.DoesNotExist:
            raise Http404
    

    def get(self, request, pk, format=None):
        salapc = self.get_object(pk)
        serializer = SalaPCSerializer(salapc)
        return Response({"status": "ok", "data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        salapc = self.get_object(pk)
        date = request.data.get("date")
        hour = request.data.get("hour")
        if date and hour and SalaPC.objects.filter(date=date, hour=hour).exclude(pk=pk).exists():
            return Response(
                {"status": "error", "message": "Ya existe una reserva para esa fecha y hora. Elige otro horario."},
                status=status.HTTP_409_CONFLICT,
            )
        serializer = SalaPCSerializer(salapc, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "Reserva de sala actualizada exitosamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Error al actualizar la SalaPC", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        salapc = self.get_object(pk)
        try:
            salapc.delete()
            return Response({"status": "ok", "message": "Reserva de sala eliminada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)