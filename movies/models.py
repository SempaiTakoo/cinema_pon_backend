from django.db import models
from django.contrib.auth import get_user_model


TAG_NAME_MAX_LEN = 128
GENRE_NAME_MAX_LEN = 128
MOVIE_TITLE_MAX_LEN = 128

User = get_user_model()


class Comment(models.Model):
    '''Модель комментария.'''
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Tag(models.Model):
    '''Модель тега.'''
    name = models.CharField(
        verbose_name='Тег',
        max_length=TAG_NAME_MAX_LEN
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Модель жанра.'''
    name = models.CharField(
        verbose_name='Жанр',
        max_length=GENRE_NAME_MAX_LEN
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class MovieGenre(models.Model):
    '''Модель связи фильмов и жанров.'''
    movie = models.ForeignKey(
        verbose_name='Фильм',
        to='Movie',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        verbose_name='Жанр',
        to='Genre',
        on_delete=models.CASCADE
    )


class Movie(models.Model):
    '''Модель фильма.'''
    title = models.CharField(
        verbose_name='Название',
        max_length=MOVIE_TITLE_MAX_LEN
    )
    genres = models.ManyToManyField(
        verbose_name='Жанры',
        to='Genre',
        through=MovieGenre,
        related_name='genres'
    )

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title


class MovieTags(models.Model):
    '''Модель связи фильмов и тегов.'''
    movie = models.ForeignKey(
        verbose_name='Фильм',
        to='Movie',
        on_delete=models.CASCADE
    )
    tags = models.ForeignKey(
        verbose_name='Тег',
        to='Tag',
        on_delete=models.CASCADE
    )


class UserMovieComment(models.Model):
    '''Модель связи комментария пользователя к фильму.'''
    author = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        null=True,
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        verbose_name='Фильм',
        to=Movie,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        verbose_name='Комментарий',
        to=Comment,
        on_delete=models.CASCADE
    )
