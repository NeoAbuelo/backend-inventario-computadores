from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.http import Http404

from ..models import Equipo
from ..serializers import EquipoSerializer

from .paginations import CustomPagination

from seguridad.decorators import logguer_required

class EquipoListCreateView(APIView):

    @logguer_required
    def get(self, request, format=None):
        equipos = Equipo.objects.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(equipos, request)
        serializer = EquipoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @logguer_required
    def post(self, request, format=None):
        serializer = EquipoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "data": "registro creado correctamente"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": "error", "message": "error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "error de validación", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class EquipoDetailView(APIView):
    
    def get_object(self, pk):
        try:
            return Equipo.objects.get(pk=pk)
        except Equipo.DoesNotExist:
            raise Http404
        
    @logguer_required
    def get(self, request, pk, format=None):
        equipo = self.get_object(pk)
        serializer = EquipoSerializer(equipo)
        return Response({"status": "ok", "data": serializer.data}, status=status.HTTP_200_OK)

    @logguer_required
    def put(self, request, pk, format=None):
        equipo = self.get_object(pk)
        serializer = EquipoSerializer(equipo, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "data": "registro actualizado correctamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "error", "message": "error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "error de validación", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    @logguer_required
    def delete(self, request, pk, format=None):
        equipo = self.get_object(pk)
        try:
            equipo.delete()
            return Response({"status": "ok", "data": "registro eliminado correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": "error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        
        
class EquipoListByDispositivoView(APIView):
    @logguer_required
    def get(self, request, dispositivo_id, format=None):
        equipos = Equipo.objects.filter(dispositivo_id=dispositivo_id).order_by('-id').all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(equipos, request)
        serializer = EquipoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)