from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Comment, MovieGenre, Tag, Genre, Movie, Comment


User = get_user_model()


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


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и чтения комментариев.'''
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Comment
        fields = (
            'author',
            'movie',
            'text'
        )


class MovieSerializer(serializers.ModelSerializer):
    '''Сериализатор для фильмов.'''
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True
    )
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
            'genres',
            # 'comments'
        )

    def get_comments(self, obj):
        comments = Comment.objects.filter(movie=obj).select_related('author')
        return [
            {
                "author": comment.author.username,
                "text": comment.text
            }
            for comment in comments
        ]

    def _set_genres(self, movie, genres_data):
        '''Создаёт в базе данных информацию о связи между фильмом и жанрами.'''

        for genre in genres_data:
            MovieGenre.objects.update_or_create(movie=movie, genre=genre)

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        self._set_genres(movie, genres_data)
        return movie

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genres', None)

        if genre_ids is not None:
            self._set_genres(instance, genre_ids)

        return instance
