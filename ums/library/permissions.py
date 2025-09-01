from rest_framework.permissions import BasePermission

class IsFacultyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('FACULTY','ADMIN'))
