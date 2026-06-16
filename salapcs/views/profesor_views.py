from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.http import Http404

from ..models import Profesor
from ..serializers import ProfesorSerializer
from .paginatios import CustomPagination


# Create your views here.
class ProfesorList(APIView):

    def get_permissions(self):
        # El listado es público (lo usa el formulario de agendamiento para el
        # desplegable de profesores). Crear profesores requiere autenticación.
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request,format=None):
        profesores = Profesor.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(profesores, request)
        serializer = ProfesorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProfesorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "Profesor creado exitosamente"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                        "status": "error",
                        "message": "Error al crear el profesor",
                        "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProfesorDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Profesor.objects.get(pk=pk)
        except Profesor.DoesNotExist:
            raise Http404
    
    def get(self, request, pk,format=None):

        profesor = self.get_object(pk)
        serializer = ProfesorSerializer(profesor)
        return Response({
            "status": "ok",
            "data": serializer.data}, status=status.HTTP_200_OK)


    def put(self, request, pk, format=None):
        profesor = self.get_object(pk)
        serializer = ProfesorSerializer(profesor, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "Profesor actualizado exitosamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                        "status": "error",
                        "message": "Error al actualizar el profesor",
                        "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk, format=None):
        profesor = self.get_object(pk)
        try:
            profesor.delete()
            return Response({"status": "ok", "message": "Profesor eliminado correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)