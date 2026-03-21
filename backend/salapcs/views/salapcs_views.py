from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from ..models import SalaPC
from ..serializers import SalaPCSerializer
from .paginatios import CustomPagination


class SalaPCList(APIView):
    def get(self, request, format=None):
        salapcs = SalaPC.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(salapcs, request)
        serializer = SalaPCSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = SalaPCSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "SalaPC created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = SalaPCSerializer(salapc, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "ok", "message": "SalaPC updated successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "error", "message": "Error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        salapc = self.get_object(pk)
        salapc.delete()
        return Response({"status": "ok", "message": "SalaPC deleted successfully"}, status=status.HTTP_204_NO_CONTENT)