from rest_framework.permissions import BasePermission

class IsHR(BasePermission):
    """Allow only HR users (ADMIN or dedicated HR role). Adjust role checks as needed."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','HR'))

class IsPayrollViewer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','HR','FACULTY'))
