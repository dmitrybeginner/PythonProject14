from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicOrOwner(BasePermission):
    """
    Разрешает чтение публичных объектов или доступ владельцу.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.is_public or obj.user == request.user
        return obj.user == request.user
