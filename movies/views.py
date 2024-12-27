from django.shortcuts import get_list_or_404

from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Comment, Tag, Genre, Director, Rating,
    Movie, MovieRecommendations, UserRecommendations
)
from .serializers import (
    CommentSerializer,
    GenreSerializer,
    DirectorSerializer,
    TagSerializer,
    MovieReadSerializer,
    MovieWriteSerializer,
    RatingSerializer,
    MovieRecommendationsReadSerializer,
    UserRecommendationsReadSerializer
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


class MovieRecommendationsViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Вьюсет для работы с рекомендациями фильмов.
    Поддерживает только операции чтения.
    '''
    queryset = MovieRecommendations.objects.all()
    serializer_class = MovieRecommendationsReadSerializer

    @action(detail=False, methods=['get'], url_path='recommendations')
    def get_recommendations_by_movie(self, request):
        movie_id = request.query_params.get('movie_id')

        if not movie_id:
            return Response(
                {'data': 'Требуется movie_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        recommendation = get_list_or_404(
            MovieRecommendations, movie__id=movie_id
        )
        return Response(
            {
                'movie_id': movie_id,
                'recommendations': recommendation.recommendations
            },
            status=status.HTTP_200_OK
        )


class UserRecommendationsViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    Вьюсет для работы с пользовательскими рекомендациями.
    Поддерживает только операции чтения.
    '''
    queryset = UserRecommendations.objects.all()
    serializer_class = UserRecommendationsReadSerializer

    @action(detail=False, methods=['get'], url_path='recommendations')
    def get_recommendations_by_user(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {'data': 'Требуется user_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        recommendation = get_list_or_404(
            UserRecommendations, user__id=user_id
        )

        return Response(
            {
                'user_id': user_id,
                'recommendations': recommendation.recommendations
            },
            status=status.HTTP_200_OK
        )


class RatingViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания, чтения, изменения и удаления рейтингов.'''
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
