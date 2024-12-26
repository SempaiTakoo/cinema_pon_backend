from rest_framework import viewsets, exceptions

from .models import Comment, Tag, Genre, Director, Movie
from .serializers import (
    CommentSerializer,
    GenreSerializer,
    DirectorSerializer,
    TagSerializer,
    MovieReadSerializer,
    MovieWriteSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления комментариев.'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TagViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления тегов.'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class GenreViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления жанров.'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class DirectorViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления режиссёров.'''
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления фильмов.'''
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return MovieReadSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return MovieWriteSerializer
        return exceptions.NotFound(
            f'Не найден сериализатор для действия {self.action}'
        )
