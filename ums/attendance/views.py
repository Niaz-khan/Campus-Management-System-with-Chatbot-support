from rest_framework import generics, permissions
from .models import Attendance
from .serializers import AttendanceSerializer
from users.permissions import IsAdmin, IsFaculty, IsStudent

# Faculty & Admin: View and mark attendance
class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    GET: List attendance records (Admin & Faculty)
    POST: Mark attendance for a student (Faculty & Admin)
    """
    queryset = Attendance.objects.select_related(
        'enrollment__student__user', 'enrollment__course', 'marked_by'
    ).all()
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsFaculty() | IsAdmin()]
        return [IsFaculty() | IsAdmin()]

# Faculty & Admin: Update/Delete attendance
class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve attendance record
    PUT/PATCH: Update attendance (Faculty & Admin)
    DELETE: Delete attendance (Admin only)
    """
    queryset = Attendance.objects.select_related(
        'enrollment__student__user', 'enrollment__course', 'marked_by'
    ).all()
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsFaculty() | IsAdmin()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsFaculty() | IsAdmin()]

# Students: View their own attendance
class MyAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Attendance.objects.filter(
            enrollment__student=self.request.user.student_profile
        )
