from django.db import models
from django.contrib.auth import get_user_model


TAG_NAME_MAX_LEN = 128
GENRE_NAME_MAX_LEN = 128
MOVIE_TITLE_MAX_LEN = 128
DIRECTOR_NAME_MAX_LEN = 128

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


class Director(models.Model):
    '''Модель режиссёра.'''
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=DIRECTOR_NAME_MAX_LEN
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=DIRECTOR_NAME_MAX_LEN
    )
    class Meta:
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

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


class MovieDirector(models.Model):
    '''Связь между фильмом и режисёром.'''
    movie = models.ForeignKey(
        verbose_name='Фильм',
        to='Movie',
        on_delete=models.CASCADE
    )
    director = models.ForeignKey(
        verbose_name='Режимссёр',
        to='Director',
        on_delete=models.CASCADE
    )


class Movie(models.Model):
    '''Модель фильма.'''
    title = models.CharField(
        verbose_name='Название',
        max_length=MOVIE_TITLE_MAX_LEN
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genres = models.ManyToManyField(
        verbose_name='Жанры',
        to='Genre',
        through=MovieGenre,
        related_name='genres'
    )
    directors = models.ManyToManyField(
        verbose_name='Режиссёры',
        to='Director',
        through=MovieDirector,
        related_name='directors'
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
