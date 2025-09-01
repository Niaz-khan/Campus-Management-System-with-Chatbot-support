from rest_framework import generics
from .models import Exam, Grade
from .serializers import ExamSerializer, GradeSerializer
from users.permissions import IsAdmin, IsFaculty, IsStudent
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Grade
from enrollments.models import Enrollment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Exam
from users.permissions import IsFaculty, IsAdmin
from notifications.utils import send_notification
from enrollments.models import Enrollment


def perform_create(self, serializer):
    exam = serializer.save(created_by=self.request.user)
    # Notify all students enrolled in the course
    enrollments = Enrollment.objects.filter(course=exam.course)
    for enrollment in enrollments:
        send_notification(
            user=enrollment.student.user,
            title="New Exam Scheduled",
            message=f"A new exam '{exam.title}' has been scheduled for {exam.date}.",
            related_object=exam
        )


class PublishExamResultsView(APIView):
    """
    Faculty/Admin: Publish exam results so students can view grades.
    """
    permission_classes = [IsFaculty | IsAdmin]

    def post(self, request, exam_id):
        exam.result_status = 'PUBLISHED'
        exam.save(update_fields=['result_status'])

        enrollments = Enrollment.objects.filter(course=exam.course)
        for enrollment in enrollments:
            send_notification(
                user=enrollment.student.user,
                title="Exam Results Published",
                message=f"Your results for '{exam.title}' are now available.",
                related_object=exam
            )
        return Response({"message": f"Results for {exam.title} published."})


class LockExamResultsView(APIView):
    """
    Admin: Lock exam results (no further edits allowed).
    """
    permission_classes = [IsAdmin]
    def post(self, request, exam_id):
        exam.result_status = 'LOCKED'
        exam.save(update_fields=['result_status'])

        enrollments = Enrollment.objects.filter(course=exam.course)
        for enrollment in enrollments:
            send_notification(
                user=enrollment.student.user,
                title="Exam Results Locked",
                message=f"Results for '{exam.title}' are now locked. No further changes will be made.",
                related_object=exam
            )
        return Response({"message": f"Results for {exam.title} locked."})


class MyGPAView(APIView):
    """
    GET: Returns the GPA for the current semester and overall CGPA for the logged-in student.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user.student_profile

        # Get all grades for this student
        all_grades = Grade.objects.filter(enrollment__student=student)

        if not all_grades.exists():
            return Response({"message": "No grades available."})

        total_points = 0
        total_credits = 0

        for grade in all_grades:
            total_points += grade.grade_point()
            total_credits += grade.enrollment.course.credit_hours

        cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0

        # Optional: calculate GPA for current semester
        current_semester = student.semester
        semester_grades = all_grades.filter(enrollment__semester=current_semester)
        sem_points = sum(g.grade_point() for g in semester_grades)
        sem_credits = sum(g.enrollment.course.credit_hours for g in semester_grades)
        gpa = round(sem_points / sem_credits, 2) if sem_credits > 0 else cgpa

        return Response({
            "GPA": gpa,
            "CGPA": cgpa,
            "credits_completed": total_credits
        })

# EXAMS MANAGEMENT
class ExamListCreateView(generics.ListCreateAPIView):
    """
    GET: List all exams (Admin, Faculty, Students)
    POST: Create a new exam (Faculty & Admin)
    """
    queryset = Exam.objects.select_related('course', 'created_by').all()
    serializer_class = ExamSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsFaculty() | IsAdmin()]
        return [IsAdmin() | IsFaculty() | IsStudent()]

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve exam details
    PUT/PATCH: Update exam (Faculty & Admin)
    DELETE: Delete exam (Admin only)
    """
    queryset = Exam.objects.select_related('course', 'created_by').all()
    serializer_class = ExamSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsFaculty() | IsAdmin()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty() | IsStudent()]

# GRADES MANAGEMENT
class GradeListCreateView(generics.ListCreateAPIView):
    """
    GET: List all grades (Admin & Faculty)
    POST: Add grade for a student (Faculty & Admin, within grading window)
    """
    queryset = Grade.objects.select_related('exam', 'enrollment').all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsFaculty() | IsAdmin()]
        return [IsAdmin() | IsFaculty()]

class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: View grade
    PUT/PATCH: Update grade (Faculty & Admin, within grading window)
    DELETE: Delete grade (Admin only)
    """
    queryset = Grade.objects.select_related('exam', 'enrollment').all()
    serializer_class = GradeSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [IsFaculty() | IsAdmin()]
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        return [IsAdmin() | IsFaculty()]

class MyGradesView(generics.ListAPIView):
    """
    GET: View logged-in student's grades
    """
    serializer_class = GradeSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return Grade.objects.filter(
            enrollment__student=self.request.user.student_profile,
            exam__result_status__in=['PUBLISHED', 'LOCKED']
        )
