from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """Пермишн проверяющий является ли пользователь владельцем привычки"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
