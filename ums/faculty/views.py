from rest_framework import generics, permissions
from .models import FacultyProfile
from .serializers import FacultyProfileSerializer
from users.permissions import IsAdmin, IsFaculty
from org_structure.models import DepartmentMember

# Admin: List or create faculty
class FacultyListCreateView(generics.ListCreateAPIView):
    """
    GET: List faculty members (filterable by campus/department)
    POST: Add a faculty profile (Admin only)
    """
    serializer_class = FacultyProfileSerializer

    def get_queryset(self):
        queryset = FacultyProfile.objects.select_related(
            'user', 'campus', 'department'
        ).all()

        campus_id = self.request.query_params.get('campus_id')
        department_id = self.request.query_params.get('department_id')

        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        user = self.request.user
        # Restrict for HOD/Coordinator to only their department
        if hasattr(user, 'departmentmember'):
            member = DepartmentMember.objects.filter(user=user, is_active=True).first()
            if member and member.role.name in ['HOD', 'COORDINATOR']:
                queryset = queryset.filter(department=member.department)

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty()]


# Admin & Faculty: View/update single faculty profile
class FacultyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve faculty profile
    PUT/PATCH: Update profile (Admin only)
    DELETE: Remove faculty (Admin only)
    """
    queryset = FacultyProfile.objects.select_related(
        'user', 'campus', 'department'
    ).all()
    serializer_class = FacultyProfileSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty()]


# Faculty: View their own profile
class MyFacultyProfileView(generics.RetrieveAPIView):
    serializer_class = FacultyProfileSerializer
    permission_classes = [IsFaculty]

    def get_object(self):
        return self.request.user.faculty_profile
