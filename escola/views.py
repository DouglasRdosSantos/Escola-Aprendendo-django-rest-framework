from escola.models import Estudante, Curso, Matricula
from escola.serializers import EstudanteSerializer, CursoSerializer, MatriculaSerializer, ListaMatriculasEstudanteSerializer, ListaMatriculasCursoSerializer, EstudanteSerializerV2
from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle
from escola.throttles import MatriculaAnonRateThrottle
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class EstudanteViewSet(viewsets.ModelViewSet):
    '''
     ViewSet para gerenciar estudantes.

    Fornece operações CRUD para o modelo Estudante, com suporte a filtragem,
    ordenação (pelo campo 'nome') e pesquisa (pelos campos 'nome' e 'cpf').

    O método `get_serializer_class` seleciona o serializer com base na versão
    da API: `EstudanteSerializerV2` para a versão 'v2' e `EstudanteSerializer`
    para outras versões.

    Attributes:
        queryset (QuerySet): Estudantes ordenados por 'id'.
        filter_backends (list): Backends de filtragem utilizados.
        ordering_fields (list): Campos para ordenação.
        search_fields (list): Campos para pesquisa.
    '''
    queryset = Estudante.objects.all().order_by('id')
    #serializer_class = EstudanteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['nome']
    search_fields = [ 'nome', 'cpf']
    def get_serializer_class(self):
        if self.request.version == 'v2':
            return EstudanteSerializerV2
        return EstudanteSerializer


class CursoViewSet(viewsets.ModelViewSet):
    '''
     ViewSet para gerenciar cursos.

    Este ViewSet fornece operações CRUD (Criar, Ler, Atualizar e Deletar) para
    o modelo Curso. Ele permite que os usuários visualizem, adicionem, atualizem
    e removam cursos.

    Attributes:
        queryset (QuerySet): Conjunto de cursos ordenados por 'id'.
        serializer_class (Serializer): Serializer utilizado para representar
        os dados do curso.
    '''
    queryset = Curso.objects.all().order_by('id')
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MatriculaViewSet(viewsets.ModelViewSet):
    '''
    ViewSet para gerenciar matrículas.

    Fornece operações para visualizar (GET) e criar (POST) matrículas. 
    Implementa limitações de taxa para usuários autenticados e anônimos.

    Attributes:
        queryset (QuerySet): Conjunto de matrículas ordenados por 'id'.
        serializer_class (Serializer): Serializer utilizado para representar os dados da matrícula.
        throttle_classes (list): Classes de limitação de taxa aplicadas.
        http_method_names (list): Métodos HTTP permitidos ('get', 'post').
    '''
    queryset = Matricula.objects.all().order_by('id')
    serializer_class = MatriculaSerializer 
    throttle_classes = [UserRateThrottle, MatriculaAnonRateThrottle]
    http_method_names = ['get', 'post']

class ListaMatriculaEstudante(generics.ListAPIView):
    '''
    Descrição da View:
    - Lista Matriculas por id de Estudante
    Parâmetros:
    - pk (int): O identificador primario do objeto. Deve ser um número inteiro
    '''

    def get_queryset(self):
        queryset = Matricula.objects.filter(estudante_id=self.kwargs['pk']).order_by('id')
        return queryset
    serializer_class = ListaMatriculasEstudanteSerializer

class ListaMatriculaCurso(generics.ListAPIView):
    '''
    Descrição da View:
    - Lista Matriculas por id de Curso
    Parâmetros:
    - pk (int): O identificador primario do objeto. Deve ser um número inteiro
    '''
     
    def get_queryset(self):
        queryset = Matricula.objects.filter(curso_id=self.kwargs['pk']).order_by('id')
        return queryset
    serializer_class = ListaMatriculasCursoSerializer



    

