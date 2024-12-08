from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания и чтения пользователей.'''

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
