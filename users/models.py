from django.contrib.auth.models import AbstractUser
from django.db import models

USERNAME_MAX_LEN = 64
PASSWORD_MAX_LEN = 256


class User(AbstractUser):
    '''Модель пользователя.'''
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=USERNAME_MAX_LEN,
        unique=True
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=PASSWORD_MAX_LEN
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
