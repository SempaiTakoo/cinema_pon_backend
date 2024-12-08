from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Comment, Tag, Genre, Director, Movie
from .serializers import (
    CommentSerializer,
    GenreSerializer,
    DirectorSerializer,
    TagSerializer,
    MovieReadSerializer,
    MovieWriteSerializer
)

class GenreListView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagListView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectorListView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DirectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления комментариев.'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Другая реализация

class Pagination(PageNumberPagination):
    '''Класс для настройки пагинации'''
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TagViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления тегов.'''
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    pagination_class = Pagination



class GenreViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления жанров.'''
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = Pagination



class DirectorViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления режиссёров.'''
    queryset = Director.objects.all().order_by('id')
    serializer_class = DirectorSerializer
    pagination_class = Pagination

class MovieViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления фильмов.'''
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return MovieReadSerializer
        if self.action in ('create', 'update'):
            return MovieWriteSerializer
        raise exceptions.NotFound(
            f'Не найден сериализатор для действия {self.action}'
        )
