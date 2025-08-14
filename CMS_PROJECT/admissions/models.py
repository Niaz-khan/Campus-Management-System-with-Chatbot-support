from django.db import models
from students.models import Student
from courses.models import Program

class AdmissionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='admission_application')
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    matric_marks = models.DecimalField(max_digits=5, decimal_places=2)
    intermediate_marks = models.DecimalField(max_digits=5, decimal_places=2)
    quota = models.CharField(max_length=50, blank=True)  # Optional: "female quota", "district quota"
    interview_date = models.DateField(null=True, blank=True)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['-applied_on']

    def __str__(self):
        return f"{self.student.roll_number} applied for {self.program.program_name} ({self.status})"
