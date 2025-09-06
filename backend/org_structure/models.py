from django.db import models
from django.conf import settings

class Campus(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('campus', 'name')

    def __str__(self):
        return f"{self.name} ({self.campus.name})"


class DepartmentRole(models.Model):
    ROLE_CHOICES = [
        ('HOD', 'Head of Department'),
        ('COORDINATOR', 'Coordinator'),
        ('CLERK', 'Clerk'),
        ('FACULTY', 'Faculty Member'),
    ]
    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class DepartmentMember(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(DepartmentRole, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('department', 'user')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name} ({self.department.name})"
