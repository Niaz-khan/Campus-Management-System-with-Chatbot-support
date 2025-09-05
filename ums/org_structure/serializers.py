from rest_framework import serializers
from .models import Campus, Department, DepartmentRole, DepartmentMember

class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'code', 'address', 'created_at']


class DepartmentSerializer(serializers.ModelSerializer):
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    class Meta:
        model = Department
        fields = ['id', 'campus', 'campus_name', 'name', 'code', 'created_at']


class DepartmentRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRole
        fields = ['id', 'name']


class DepartmentMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    role_name = serializers.CharField(source='role.get_name_display', read_only=True)

    class Meta:
        model = DepartmentMember
        fields = [
            'id', 'department', 'department_name', 'user', 'user_name',
            'role', 'role_name', 'assigned_at', 'is_active'
        ]
