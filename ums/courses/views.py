from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseSerializer
from users.permissions import IsAdmin, IsFaculty

# List & create courses
class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET: List all courses
    POST: Create a new course (Admin only)
    """
    queryset = Course.objects.select_related('program', 'batch', 'faculty').all()
    serializer_class = CourseSerializer

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
    queryset = Course.objects.select_related('program', 'batch', 'faculty').all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdmin() | IsFaculty()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]
