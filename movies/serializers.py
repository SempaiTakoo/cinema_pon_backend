from rest_framework import serializers

from users.models import User

from .models import (
    Comment, Rating, Tag, Genre, Director,
    Movie, MovieRecommendations, UserRecommendations
)


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и чтения тегов.'''

    class Meta:
        model = Tag
        fields = (
            'id',
            'name'
        )


class GenreSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и изменения жанров.'''

    class Meta:
        model = Genre
        fields = (
            'id',
            'name'
        )

class DirectorSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и изменения режиссёров.'''

    class Meta:
        model = Director
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class MovieReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения фильмов.'''
    genres = GenreSerializer(many=True)
    directors = DirectorSerializer(many=True)


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и чтения комментариев.'''
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Comment
        fields = ('author', 'movie', 'text')


class MovieReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения фильмов.'''
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True
    )
    directors = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(), many=True
    )
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'genres', 'directors', 'comments'
        )
        read_only_fields = (
            'id', 'title', 'description', 'genres', 'directors', 'comments'
        )

    def get_comments(self, obj):
        comments = Comment.objects.filter(movie=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class MovieWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и изменения фильмов.'''
    genres = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    directors = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'description',
            'genres',
            'directors'
        )
        extra_kwargs = {
            'title': {'write_only': True},
            'description': {'write_only': True},
            'genres': {'write_only': True},
            'directors': {'write_only': True}
        }

    def _set_genres(self, movie, genre_ids):
        '''Создаёт в базе данных информацию о связи между фильмом и жанрами.'''
        genres = Genre.objects.filter(id__in=genre_ids)
        movie.genres.set(genres)

    def _set_directors(self, movie, director_ids):
        '''
        Создаёт в базе данных информацию о связи между фильмом и директором.
        '''
        directors = Director.objects.filter(id__in=director_ids)
        movie.directors.set(directors)

    def create(self, validated_data):
        genre_ids = validated_data.pop('genres',[])
        director_ids = validated_data.pop('directors',[])
        movie = Movie.objects.create(**validated_data)
        self._set_genres(movie, genre_ids)
        self._set_directors(movie, director_ids)
        return movie

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genres', None)
        director_ids = validated_data.pop('directors', None)

        if genre_ids is not None:
            self._set_genres(instance, genre_ids)

        if director_ids is not None:
            self._set_directors(instance, director_ids)

        return instance


class MovieRecommendationsReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения рекомендаций для фильмов.'''
    class Meta:
        model = MovieRecommendations
        fields = ('movie', 'recommendations')


class UserRecommendationsReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения рекомендаций для пользователей.'''
    class Meta:
        model = UserRecommendations
        fields = ('user', 'recommendations')


class RatingSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и чтения рейтингов.'''
    class Meta:
        model = Rating
        fields = ('id', 'rating', 'movie', 'author', 'created_at')
