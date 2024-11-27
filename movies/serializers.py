from rest_framework import serializers
from rest_framework import exceptions

from .models import Comment, Tag, Genre, Movie, UserMovieComment


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и чтения комментариев.'''

    class Meta:
        model = Comment
        fields = (
            'text',
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


class MovieReadSerializer(serializers.ModelSerializer):
    '''Сериализатор для чтения фильмов.'''
    genres = GenreSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'genres',
            'comments'
        )
        read_only_fields = (
            'id',
            'title',
            'genres',
            'comments'
        )

    def get_comments(self, obj):
        return UserMovieComment.objects.filter(movie=obj)


class MovieWriteSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и изменения фильмов.'''
    genres = serializers.SerializerMethodField

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'genres'
        )
        extra_kwargs = {
            'title': {'write_only': True},
            'genres': {'write_only': True}
        }

    def _set_genres(self, movie, genre_ids):
        '''Создаёт в базе данных информацию о связи между фильмом и жанрами.'''
        genres = Genre.objects.filter(id__in=genre_ids)

        if len(genres) != len(genre_ids):
            wrong_genres = set(genre_ids) - set(genre.id for genre in genres)
            raise exceptions.ValidationError(
                f'Неверные или несуществующие ID жанров: {wrong_genres}'
            )

        movie.genres.set(genres)

    def create(self, validated_data):
        genre_ids = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        self._set_genres(movie, genre_ids)
        return movie

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genres', None)

        if genre_ids is not None:
            self._set_genres(instance, genre_ids)

        return instance
