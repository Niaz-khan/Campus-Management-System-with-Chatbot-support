from rest_framework import generics, permissions
from .models import Attendance
from .serializers import AttendanceSerializer
from attendance.permissions import IsFaculty


class FacultyAttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsFaculty]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)


class FacultyAttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsFaculty]

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        queryset = Attendance.objects.all()
        if course_id:
            queryset = queryset.filter(enrollment__course_id=course_id)
        return queryset


class FacultyAttendanceUpdateView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsFaculty]



class StudentAttendanceListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.filter(enrollment__student__user=user)

        # Optional filters
        course_id = self.request.query_params.get('course')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if course_id:
            queryset = queryset.filter(enrollment__course_id=course_id)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        return queryset
