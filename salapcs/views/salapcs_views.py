from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from ..models import SalaPC
from ..serializers import SalaPCSerializer
from .paginatios import CustomPagination

from seguridad.decorators import logguer_required

    
class SalaPCList(APIView):
    @logguer_required
    def get(self, request, format=None):
        salapcs = SalaPC.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(salapcs, request)
        serializer = SalaPCSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    @logguer_required
    def post(self, request, format=None):
        serializer = SalaPCSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "SalaPC created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Error al crear la SalaPC", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SalaPCDetail(APIView):
    def get_object(self, pk):
        try:
            return SalaPC.objects.get(pk=pk)
        except SalaPC.DoesNotExist:
            raise Http404
    

    @logguer_required
    def get(self, request, pk, format=None):
        salapc = self.get_object(pk)
        serializer = SalaPCSerializer(salapc)
        return Response({"status": "ok", "data": serializer.data}, status=status.HTTP_200_OK)
    

    @logguer_required
    def put(self, request, pk, format=None):
        salapc = self.get_object(pk)
        serializer = SalaPCSerializer(salapc, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "SalaPC updated successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Error al actualizar la SalaPC", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    @logguer_required
    def delete(self, request, pk, format=None):
        salapc = self.get_object(pk)
        try:
            salapc.delete()
            return Response({"status": "ok", "message": "SalaPC deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)