from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.db.models import Avg, Sum
from .models import ParentProfile, ParentStudentLink
from students.models import StudentProfile
from attendance.models import Attendance
from fees.models import Invoice
from exams.models import Grade
from notifications.models import Notification
from .serializers import ParentProfileSerializer, ParentStudentLinkSerializer, ParentDashboardSerializer

class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'PARENT')

# 1. View own parent profile
class ParentProfileView(generics.RetrieveAPIView):
    serializer_class = ParentProfileSerializer
    permission_classes = [IsParent]

    def get_object(self):
        return self.request.user.parent_profile

# 2. List linked students
class ParentLinkedStudentsView(generics.ListAPIView):
    serializer_class = ParentStudentLinkSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return ParentStudentLink.objects.filter(parent=self.request.user.parent_profile)

# 3. Child dashboard
class ParentStudentDashboardView(generics.RetrieveAPIView):
    serializer_class = ParentDashboardSerializer
    permission_classes = [IsParent]

    def retrieve(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        try:
            student = StudentProfile.objects.get(id=student_id, linked_parents__parent=request.user.parent_profile)
        except StudentProfile.DoesNotExist:
            return Response({"detail": "Student not linked to your account."}, status=status.HTTP_404_NOT_FOUND)

        # Calculate attendance
        total_attendance = Attendance.objects.filter(enrollment__student=student).count()
        present_attendance = Attendance.objects.filter(enrollment__student=student, status='PRESENT').count()
        attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0

        # Calculate fees due
        total_fees_due = Invoice.objects.filter(student=student, is_paid=False).aggregate(total=Sum('amount'))['total'] or 0

        # Latest grades
        latest_grades = list(Grade.objects.filter(student=student).order_by('-created_at')[:5].values('course__name', 'grade'))

        # Unread notifications
        unread_notifications = Notification.objects.filter(user=student.user, is_read=False).count()

        data = {
            "student": student,
            "attendance_percentage": attendance_percentage,
            "total_fees_due": total_fees_due,
            "latest_grades": latest_grades,
            "unread_notifications": unread_notifications,
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)
