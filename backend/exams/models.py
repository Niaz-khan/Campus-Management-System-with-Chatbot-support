from django.db import models
from django.conf import settings
from datetime import timedelta, date
from courses.models import Course
from enrollments.models import Enrollment

def percentage_to_grade_point(percentage: float) -> float:
    """
    Converts percentage to grade point based on a standard 4.0 scale.
    Adjust scale according to university policy if needed.
    """
    if percentage >= 85:
        return 4.0
    elif percentage >= 80:
        return 3.7
    elif percentage >= 75:
        return 3.3
    elif percentage >= 70:
        return 3.0
    elif percentage >= 65:
        return 2.7
    elif percentage >= 60:
        return 2.3
    elif percentage >= 55:
        return 2.0
    elif percentage >= 50:
        return 1.7
    else:
        return 0.0


class Exam(models.Model):
    EXAM_TYPES = [
        ('MIDTERM', 'Midterm'),
        ('FINAL', 'Final'),
        ('QUIZ', 'Quiz'),
        ('ASSIGNMENT', 'Assignment'),
    ]
    RESULT_STATUS = [
        ('DRAFT', 'Draft'),       # Faculty entering grades
        ('PUBLISHED', 'Published'),  # Students can view grades
        ('LOCKED', 'Locked'),     # No further edits allowed
    ]
    result_status = models.CharField(
        max_length=10,
        choices=RESULT_STATUS,
        default='DRAFT'
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='MIDTERM')
    total_marks = models.PositiveIntegerField(default=100)
    date = models.DateField()
    grading_deadline_days = models.PositiveIntegerField(default=30)  # e.g., 15–30 days
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'FACULTY'},
        related_name="created_exams"
    )

    def grading_deadline(self):
        return self.date + timedelta(days=self.grading_deadline_days)

    def grade_point(self):
        """Returns the grade points earned for this exam based on marks percentage."""
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
        return percentage_to_grade_point(percentage) * self.enrollment.course.credit_hours
        today = date.today()
        return self.date <= today <= self.grading_deadline()
    def can_edit_grades(self):
        """
        Grades can be added/updated only if the result is in DRAFT
        and within the grading window.
        """
        return self.result_status == 'DRAFT' and self.can_accept_grades()

    def can_students_view(self):
        """
        Students can only view grades if results are published or locked.
        """
        return self.result_status in ['PUBLISHED', 'LOCKED']

    def __str__(self):
        return f"{self.title} - {self.course.code}"

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="grades")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="grades")
    marks_obtained = models.FloatField()
    remarks = models.TextField(blank=True, null=True)
    
    def grade_point(self):
        """Returns the grade points earned for this exam based on marks percentage."""
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
        return percentage_to_grade_point(percentage) * self.enrollment.course.credit_hours

    class Meta:
        unique_together = ("enrollment", "exam")

    def __str__(self):
        return f"{self.enrollment.student.roll_no} - {self.exam.title} ({self.marks_obtained})"
