from django.shortcuts import render
from rest_framework import generics, permissions
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from users.permissions import IsAdmin, IsFaculty
from org_structure.models import DepartmentMember

# Admin and Faculty can list students with filtering
class StudentListView(generics.ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdmin | IsFaculty]

    def get_queryset(self):
        queryset = StudentProfile.objects.select_related(
            'user', 'batch', 'program', 'campus', 'department'
        ).all()

        campus_id = self.request.query_params.get('campus_id')
        department_id = self.request.query_params.get('department_id')

        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        user = self.request.user

        # Restrict Faculty to their department if they are HOD or Coordinator
        if hasattr(user, 'departmentmember'):
            member = DepartmentMember.objects.filter(user=user, is_active=True).first()
            if member and member.role.name in ['HOD', 'COORDINATOR']:
                queryset = queryset.filter(department=member.department)

        return queryset


# Retrieve or update a single student profile
class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = StudentProfile.objects.select_related(
        'user', 'batch', 'program', 'campus', 'department'
    ).all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAdmin | IsFaculty]


# For students to view their own profile
class MyStudentProfileView(generics.RetrieveAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.student_profile
