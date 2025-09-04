from django.db import models
from django.conf import settings
from students.models import StudentProfile

class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Parent: {self.user.get_full_name()}"

class ParentStudentLink(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='linked_students')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='linked_parents')
    relation = models.CharField(max_length=50, help_text="e.g., Father, Mother, Guardian")
    linked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'student')

    def __str__(self):
        return f"{self.parent.user.get_full_name()} → {self.student.roll_no}"
