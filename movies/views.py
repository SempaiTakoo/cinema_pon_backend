from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Comment, Tag, Genre, Movie
from .serializers import (
    CommentSerializer,
    GenreSerializer,
    MovieSerializer,
    TagSerializer
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
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления комментариев.'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Другая реализация
class TagViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления тегов.'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class GenreViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удалениях жанров.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления фильмов.'''
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
