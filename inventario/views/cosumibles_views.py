from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404

from ..models import Consumible
from ..serializers import ConsumibleSerializer

from .paginations import CustomPagination


class ConsumibleList(APIView):

    def get(self, request, format=None):
        consumibles = Consumible.objects.all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(consumibles, request)
        serializer = ConsumibleSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):
        
        data = ConsumibleSerializer(data=request.data)
        
        if data.is_valid():
            try:
                data.save()
                return Response({"status" : "ok",
                                    "message":"Registro creado exitosamente"},
                                     status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "status" : "error",
                    "message": "Error inesperado"
                    },status=status.HTTP_400_BAD_REQUEST)
                    
        return Response({
            "status" : "error",
            "message": data.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class ConsumibleDetail(APIView):

    def get_object(self,pk):
        try:
           return Consumible.objects.get(pk=pk)
        except Consumible.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None ):
        consumible = self.get_object(pk)
        data_json = ConsumibleSerializer(consumible)
        return Response({"status":"ok",
                         "data":data_json.data},status=status.HTTP_200_OK)
    
    def put(self, request, pk, format=None):
        consumible = self.get_object(pk)
        data = ConsumibleSerializer(consumible, data=request.data)
        
        if data.is_valid():
            try:
                data.save()
                return Response({"status" : "ok",
                                    "message":"Registro actualizado exitosamente"},
                                     status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "status" : "error",
                    "message": "Error inesperado"
                    },status=status.HTTP_400_BAD_REQUEST)
                    
        return Response({
            "status" : "error",
            "message": data.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        consumible = self.get_object(pk)
        try:
            consumible.delete()
            return Response({"status" : "ok",
                                "message":"Registro eliminado exitosamente"},
                                 status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status" : "error",
                "message": "Error inesperado"
                },status=status.HTTP_400_BAD_REQUEST)