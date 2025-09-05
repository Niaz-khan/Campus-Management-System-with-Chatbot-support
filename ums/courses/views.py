from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseSerializer
from users.permissions import IsAdmin, IsFaculty
from org_structure.models import DepartmentMember

# List & create courses
class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET: List courses (filterable by campus & department)
    POST: Create a new course (Admin only)
    """
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.select_related(
            'program', 'batch', 'faculty', 'campus', 'department'
        ).all()

        campus_id = self.request.query_params.get('campus_id')
        department_id = self.request.query_params.get('department_id')

        if campus_id:
            queryset = queryset.filter(campus_id=campus_id)
        if department_id:
            queryset = queryset.filter(department_id=department_id)

        user = self.request.user
        # Restrict for HOD/Coordinator
        if hasattr(user, 'departmentmember'):
            member = DepartmentMember.objects.filter(user=user, is_active=True).first()
            if member and member.role.name in ['HOD', 'COORDINATOR']:
                queryset = queryset.filter(department=member.department)

        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]


# Retrieve, update, delete course
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a course
    PUT/PATCH: Update course (Admin or Faculty assigned)
    DELETE: Delete course (Admin only)
    """
    queryset = Course.objects.select_related(
        'program', 'batch', 'faculty', 'campus', 'department'
    ).all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdmin() | IsFaculty()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
