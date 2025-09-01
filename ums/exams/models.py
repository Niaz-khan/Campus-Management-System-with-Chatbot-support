from django.db import models
from django.conf import settings
from courses.models import Course
from enrollments.models import Enrollment

class Exam(models.Model):
    EXAM_TYPES = [
        ('MIDTERM', 'Midterm'),
        ('FINAL', 'Final'),
        ('QUIZ', 'Quiz'),
        ('ASSIGNMENT', 'Assignment'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='MIDTERM')
    total_marks = models.PositiveIntegerField(default=100)
    date = models.DateField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'FACULTY'},
        related_name="created_exams"
    )

    def __str__(self):
        return f"{self.title} - {self.course.code}"

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="grades")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="grades")
    marks_obtained = models.FloatField()
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("enrollment", "exam")

    def __str__(self):
        return f"{self.enrollment.student.roll_no} - {self.exam.title} ({self.marks_obtained})"
