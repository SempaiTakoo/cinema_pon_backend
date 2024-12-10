from rest_framework import permissions

from users.models import User


class IsAuthorOrAdmin(permissions.BasePermission):
    '''Разрешение доступа для автора объекта или  .'''

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return (
            request.user and request.user.is_staff
            or request.user == obj.author
        )
