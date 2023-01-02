from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from cursos.models import Curso, Avaliacao
from cursos.serializers import CursoSerializer, AvaliacaoSerializer
# Create your views here.

class CursoAPIView(APIView):
    """
    API de Cursos da Geek
    """
    def get(self,request:Request):
        cursos = Curso.objects.all()
        serializer = CursoSerializer(cursos,many=True)
        return Response(serializer.data)
    
    def post(self,request:Request):
        serializer = CursoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class AvaliacaoAPIView(APIView):
    """
    API de Avaliações da Geek
    """
    def get(self,request:Request):
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes,many=True)
        return Response(serializer.data)
    
    def post(self,request:Request):
        serializer = AvaliacaoSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)