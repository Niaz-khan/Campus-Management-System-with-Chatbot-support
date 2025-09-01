from django.db import models
from django.conf import settings
from enrollments.models import Enrollment

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="attendance_records")
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'FACULTY'},
        related_name="marked_attendance"
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("enrollment", "date")
        ordering = ['-date']

    def __str__(self):
        return f"{self.enrollment.student.roll_no} - {self.enrollment.course.code} - {self.date} ({self.status})"
