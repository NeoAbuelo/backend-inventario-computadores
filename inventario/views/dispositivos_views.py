from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404

from ..models import Dispositivo
from ..serializers import DispositivoSerializer

from .paginations import CustomPagination

from seguridad.decorators import logguer_required

class DispositivoList(APIView):

    @logguer_required
    def get(self, request, format=None):
        dispositivos = Dispositivo.objects.order_by('-id').all()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(dispositivos, request)
        serializer = DispositivoSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @logguer_required
    def post(self, request, format=None):
        
        data = DispositivoSerializer(data=request.data)
        
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

class DispositivoDetail(APIView):

    def get_object(self,pk):
        try:
           return Dispositivo.objects.get(pk=pk)
        except Dispositivo.DoesNotExist:
            raise Http404
    
    @logguer_required
    def get(self, request, pk, format=None ):
        dispositivo = self.get_object(pk)
        data_json = DispositivoSerializer(dispositivo)
        return Response({"status":"ok",
                         "data":data_json.data},status=status.HTTP_200_OK)
    
    @logguer_required
    def put(self,request,pk, format=None):
        dispositivo = self.get_object(pk)
        data = DispositivoSerializer(dispositivo, data=request.data)
        
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
    

    @logguer_required
    def delete(self, request, pk, format=None):
        dispositivo = self.get_object(pk)
        try:
            dispositivo.delete()
            return Response({"status":"ok",
                                 "message":"Registro eliminado exitosamente"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                    "status" : "error",
                    "message": "Error inesperado"
                    },status=status.HTTP_400_BAD_REQUEST)
        

