from rest_framework.permissions import BasePermission
from .models import DepartmentMember

class CanManageMembers(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Check if user has a role with can_manage_members=True
        return DepartmentMember.objects.filter(
            user=request.user,
            role__can_manage_members=True,
            is_active=True
        ).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Only within their department
        return (
            hasattr(obj, 'department') and
            DepartmentMember.objects.filter(
                user=request.user,
                department=obj.department,
                role__can_manage_members=True,
                is_active=True
            ).exists()
        )
