from rest_framework import permissions, viewsets

from .models import User
from .serializers import CustomUserSerializer
from .permissions import IsAuthorOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет пользователя.'''
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return IsAuthorOrAdmin
        return(permissions.IsAdminUser,)
