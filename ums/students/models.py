from django.db import models
from django.conf import settings
from academics.models import Batch, Program

class StudentProfile(models.Model):
    """
    Stores detailed information for students.
    Linked to the custom User model via OneToOneField.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, related_name="students")
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, related_name="students")
    roll_no = models.CharField(max_length=20, unique=True)
    semester = models.PositiveIntegerField(default=1)
    section = models.CharField(max_length=10, blank=True, null=True)
    admission_date = models.DateField(auto_now_add=True)
    gpa = models.FloatField(default=0.0)
    cgpa = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.roll_no}"
