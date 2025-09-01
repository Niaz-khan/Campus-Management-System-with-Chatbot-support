from django.db import models
from students.models import StudentProfile
from courses.models import Course

class Enrollment(models.Model):
    """
    Represents a student's enrollment in a specific course.
    """
    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('DROPPED', 'Dropped'),
        ('COMPLETED', 'Completed'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENROLLED')
    grade = models.CharField(max_length=5, blank=True, null=True)  # e.g., A, B+, C

    class Meta:
        unique_together = ("student", "course")  # Prevents duplicate enrollments

    def __str__(self):
        return f"{self.student.roll_no} - {self.course.code} ({self.status})"
