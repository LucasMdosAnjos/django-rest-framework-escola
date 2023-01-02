from rest_framework import generics
from rest_framework.generics import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from .models import Curso, Avaliacao
from .serializers import CursoSerializer, AvaliacaoSerializer


"""
API V1
"""

# Lista a coleção (todos) e cria objeto
class CursosAPIView(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Lista, atualiza e detroi um único objeto


class CursoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class AvaliacoesAPIView(generics.ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

    #sobrescrever o metodo da classe para aceitar parametros com nome diferente de pk (como avaliacao_pk ou curso_pk) 
    def get_queryset(self):
        if self.kwargs.get('curso_pk'):
            return self.queryset.filter(curso_id=self.kwargs.get('curso_pk'))
        return self.queryset.all()


class AvaliacaoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer


    #sobrescrever o metodo da classe para aceitar parametros com nome diferente de pk (como avaliacao_pk ou curso_pk) 
    def get_object(self):
        if self.kwargs.get('curso_pk'):
            return get_object_or_404(self.get_queryset(), curso_id=self.kwargs.get('curso_pk'), pk=self.kwargs.get('avaliacao_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('avaliacao_pk'))

"""
API V2
"""
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    pagination_class = LargeResultsSetPagination

    def list(self,request:Request):
        #caso possua filtro aplica
        if('filtro' in request.query_params):
            filtro = request.query_params['filtro']
            #query para filtrar por titulo ou url caso contenha
            query = Q(titulo__contains=filtro)
            query.add(Q(url__contains=filtro),Q.OR)
            #pegar a pagina
            page = self.paginate_queryset(self.queryset.filter(query))
            if page is not None:
                serializer = self.get_serializer(page,many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(self.queryset.filter(query))
            return Response(serializer.data)
        #se não tiver filtro vai tudo
        else:
            page = self.paginate_queryset(self.queryset)
            if page is not None:
                serializer = self.serializer_class(page,many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.serializer_class(self.queryset)
            return Response(serializer.data)

    @action(detail=True,methods=['GET'])
    def avaliacoes(self,request:Request,pk=None):
        avaliacoes = Avaliacao.objects.filter(curso=pk)
        page = self.paginate_queryset(avaliacoes)
        if page is not None:
            serializer = AvaliacaoSerializer(page,many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AvaliacaoSerializer(avaliacoes)
        return Response(serializer.data)

"""
class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer 
"""

class AvaliacaoViewSet(
mixins.ListModelMixin,
mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
viewsets.GenericViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    pagination_class = LargeResultsSetPagination