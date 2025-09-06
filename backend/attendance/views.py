from rest_framework import generics, permissions
from .models import Attendance
from .serializers import AttendanceSerializer
from attendance.permissions import IsFaculty, IsAdmin
from org_structure.models import DepartmentMember


class FacultyAttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsFaculty]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)


# Faculty: View and mark attendance
class AttendanceFacultyListView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdmin | IsFaculty]

    def get_queryset(self):
        queryset = Attendance.objects.select_related(
            'enrollment', 'enrollment__course',
            'enrollment__course__campus',
            'enrollment__course__department'
        ).all()

        campus_id = self.request.query_params.get('campus_id')
        department_id = self.request.query_params.get('department_id')

        if campus_id:
            queryset = queryset.filter(enrollment__course__campus_id=campus_id)
        if department_id:
            queryset = queryset.filter(enrollment__course__department_id=department_id)

        user = self.request.user
        if hasattr(user, 'departmentmember'):
            member = DepartmentMember.objects.filter(user=user, is_active=True).first()
            if member and member.role.name in ['HOD', 'COORDINATOR']:
                queryset = queryset.filter(enrollment__course__department=member.department)

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
