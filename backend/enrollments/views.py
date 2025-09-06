from rest_framework import generics, permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer
from users.permissions import IsAdmin, IsFaculty, IsStudent

# Admin & Faculty: View all enrollments
class EnrollmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all enrollments
    POST: Enroll a student in a course (Admin only)
    """
    queryset = Enrollment.objects.select_related('student__user', 'course').all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty()]

# Admin & Faculty: View/update/delete single enrollment
class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve enrollment
    PUT/PATCH: Update enrollment (Admin or Faculty)
    DELETE: Remove enrollment (Admin only)
    """
    queryset = Enrollment.objects.select_related('student__user', 'course').all()
    serializer_class = EnrollmentSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsAdmin() | IsFaculty()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty()]

# Students: View their own enrollments
class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user.student_profile)
