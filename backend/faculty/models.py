from django.db import models
from django.conf import settings
from academics.models import Program, Batch
from org_structure.models import Campus, Department

class FacultyProfile(models.Model):
    """
    Stores detailed information about faculty members.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="faculty_profile")
    designation = models.CharField(max_length=50)  # e.g., Professor, Lecturer
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, related_name="faculty_members")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="faculty_members")
    office_room = models.CharField(max_length=50, blank=True, null=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.designation}"
