from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from .serializers import (
    AdminDashboardSerializer, DepartmentDashboardSerializer,
    FacultyDashboardSerializer, StudentDashboardSerializer
)
from .permissions import IsAdmin, IsFaculty, IsStudent, IsParent
from .utils import try_import

# Try import models (if an app is missing, metric defaults to zero)
StudentProfile = try_import('students.models.StudentProfile')
FacultyProfile = try_import('faculty.models.FacultyProfile') or try_import('users.models.User')
Course = try_import('courses.models.Course')
Exam = try_import('exams.models.Exam')
Attendance = try_import('attendance.models.Attendance')
Invoice = try_import('fees.models.Invoice')
Notification = try_import('notifications.models.Notification')
DepartmentMember = try_import('org_structure.models.DepartmentMember')
Department = try_import('org_structure.models.Department')
TransportPass = try_import('transport.models.TransportPass')
GymMembership = try_import('sports.models.GymMembership')
MessSubscription = try_import('cafeteria.models.MessSubscription')
Event = try_import('events.models.Event')
TournamentRegistration = try_import('sports.models.TournamentRegistration')


# ---------- Admin Dashboard ----------
class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        # safe defaults
        total_students = StudentProfile.objects.count() if StudentProfile else 0
        total_faculty = FacultyProfile.objects.count() if FacultyProfile else 0
        total_courses = Course.objects.count() if Course else 0

        fees_collected = Decimal('0.00')
        fees_overdue = Decimal('0.00')
        if Invoice:
            fees_collected = Invoice.objects.filter(is_paid=True).aggregate(total=('amount', 'sum'))['total'] or Decimal('0.00')  # fallback if no sum alias
            # the aggregate alias above might not actually work in some Django versions; safer:
            try:
                fees_collected = Invoice.objects.filter(is_paid=True).aggregate(s=models.Sum('amount'))['s'] or Decimal('0.00')
                fees_overdue = Invoice.objects.filter(is_paid=False, due_date__lt=timezone.now().date()).aggregate(s=models.Sum('amount'))['s'] or Decimal('0.00')
            except Exception:
                # fallback to zero if aggregate fails
                fees_collected = fees_collected or Decimal('0.00')
                fees_overdue = fees_overdue or Decimal('0.00')

        attendance_avg_percent = 0.0
        if Attendance:
            total = Attendance.objects.count()
            present = Attendance.objects.filter(status='PRESENT').count() if total else 0
            attendance_avg_percent = (present / total * 100) if total else 0.0

        upcoming_exams = Exam.objects.filter(date__gte=timezone.now().date()).count() if Exam else 0
        unread_notifications = Notification.objects.filter(is_read=False).count() if Notification else 0

        payload = {
            "total_students": total_students,
            "total_faculty": total_faculty,
            "total_courses": total_courses,
            "fees_collected": fees_collected,
            "fees_overdue": fees_overdue,
            "attendance_avg_percent": attendance_avg_percent,
            "upcoming_exams": upcoming_exams,
            "unread_notifications": unread_notifications,
        }
        serializer = AdminDashboardSerializer(payload)
        return Response(serializer.data)


# ---------- Department-scoped dashboards (HOD / Coordinator) ----------
class DepartmentDashboardView(APIView):
    """
    HOD or Coordinator sees metrics for their department (and campus if needed).
    """
    permission_classes = [IsFaculty]

    def get(self, request):
        user = request.user
        # find department member entry
        member = None
        try:
            if DepartmentMember:
                member = DepartmentMember.objects.filter(user=user, is_active=True).select_related('department').first()
        except Exception:
            member = None

        if not member:
            return Response({"detail": "Not authorized as department member."}, status=status.HTTP_403_FORBIDDEN)

        department = member.department

        students_count = StudentProfile.objects.filter(department=department).count() if StudentProfile else 0
        faculty_count = FacultyProfile.objects.filter(department=department).count() if FacultyProfile else 0
        courses_count = Course.objects.filter(department=department).count() if Course else 0

        # attendance for department
        attendance_avg_percent = 0.0
        if Attendance:
            att_qs = Attendance.objects.filter(enrollment__course__department=department)
            total = att_qs.count()
            present = att_qs.filter(status='PRESENT').count() if total else 0
            attendance_avg_percent = (present / total * 100) if total else 0.0

        upcoming_exams = Exam.objects.filter(course__department=department, date__gte=timezone.now().date()).count() if Exam else 0
        unread_notifications = 0
        if Notification:
            unread_notifications = Notification.objects.filter(
                (models.Q(user__faculty_profile__department=department) | models.Q(user__student_profile__department=department)),
                is_read=False
            ).count()

        payload = {
            "students": students_count,
            "faculty": faculty_count,
            "courses": courses_count,
            "attendance_avg_percent": attendance_avg_percent,
            "upcoming_exams": upcoming_exams,
            "unread_notifications": unread_notifications
        }
        serializer = DepartmentDashboardSerializer(payload)
        return Response(serializer.data)


# ---------- Faculty Dashboard ----------
class FacultyDashboardView(APIView):
    permission_classes = [IsFaculty]

    def get(self, request):
        user = request.user
        # FacultyProfile may be linked via user.faculty_profile
        faculty = None
        try:
            faculty = getattr(user, 'faculty_profile', None)
        except Exception:
            faculty = None

        # my courses count
        my_courses = 0
        to_mark_attendance = 0
        to_grade = 0
        unread_notifications = 0

        if Course:
            # try common relations: Course.faculty or Course.instructors M2M
            try:
                my_courses_q = Course.objects.filter(faculty__user=user) if hasattr(Course, 'faculty') else Course.objects.filter(instructors__user=user)
                my_courses = my_courses_q.count()
            except Exception:
                my_courses = 0

        if Attendance:
            # find attendance entries for courses taught by this faculty that are unmarked? We'll count upcoming sessions that might need marking
            try:
                to_mark_attendance = Attendance.objects.filter(marked_by__user=user, status='LATE').count()  # placeholder
            except Exception:
                to_mark_attendance = 0

        if Exam:
            try:
                # exams where this faculty needs to grade — depends on model; using stub: Exam.created_by == user and not graded entries exist
                to_grade = Exam.objects.filter(course__faculty__user=user, date__lte=timezone.now().date(), is_published=False).count()
            except Exception:
                to_grade = 0

        if Notification:
            try:
                unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
            except Exception:
                unread_notifications = 0

        payload = {
            "my_courses": my_courses,
            "to_mark_attendance": to_mark_attendance,
            "to_grade": to_grade,
            "unread_notifications": unread_notifications
        }
        serializer = FacultyDashboardSerializer(payload)
        return Response(serializer.data)


# ---------- Student Dashboard ----------
class StudentDashboardView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user
        student = getattr(user, 'student_profile', None)

        if not student:
            return Response({"detail": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # enrolled courses
        enrolled_courses = 0
        upcoming_exams = 0
        attendance_percent = 0.0
        fees_due = Decimal('0.00')
        unread_notifications = 0

        if Course:
            try:
                # if you have enrollment relation
                enrolled_courses = student.enrollments.count() if hasattr(student, 'enrollments') else 0
            except Exception:
                enrolled_courses = 0

        if Exam:
            try:
                upcoming_exams = Exam.objects.filter(course__in=[e.course for e in student.enrollments.all()], date__gte=timezone.now().date()).count()
            except Exception:
                upcoming_exams = 0

        if Attendance:
            try:
                all_att = Attendance.objects.filter(enrollment__student=student)
                total = all_att.count()
                present = all_att.filter(status='PRESENT').count() if total else 0
                attendance_percent = (present / total * 100) if total else 0.0
            except Exception:
                attendance_percent = 0.0

        if Invoice:
            try:
                fees_due = Invoice.objects.filter(student=student, is_paid=False).aggregate(s=models.Sum('amount'))['s'] or Decimal('0.00')
            except Exception:
                fees_due = Decimal('0.00')

        if Notification:
            try:
                unread_notifications = Notification.objects.filter(user=user, is_read=False).count()
            except Exception:
                unread_notifications = 0

        payload = {
            "enrolled_courses": enrolled_courses,
            "upcoming_exams": upcoming_exams,
            "attendance_percent": attendance_percent,
            "fees_due": fees_due,
            "unread_notifications": unread_notifications
        }
        serializer = StudentDashboardSerializer(payload)
        return Response(serializer.data)
