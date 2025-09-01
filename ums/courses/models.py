from django.db import models
from academics.models import Program, Batch
from django.conf import settings

class Course(models.Model):
    """
    Represents a course offered in a program (and optionally a specific batch).
    """
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="courses")
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses")
    code = models.CharField(max_length=20, unique=True)  # e.g., CS101
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField(default=3)
    semester = models.PositiveIntegerField()  # e.g., 1 for first semester
    course_type = models.CharField(
        max_length=20,
        choices=[('CORE', 'Core'), ('ELECTIVE', 'Elective')],
        default='CORE'
    )
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'FACULTY'},
        related_name="teaching_courses"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"
