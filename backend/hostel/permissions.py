from rest_framework.permissions import BasePermission

class IsAdminOrHostelStaff(BasePermission):
    """
    Hostel staff may be Admin or Faculty. Adjust logic if you have a specific hostel-staff role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ('ADMIN','FACULTY'))

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'STUDENT')
