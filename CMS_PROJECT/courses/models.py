from django.db import models

class Program(models.Model):
    program_name = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    duration_years = models.PositiveIntegerField()
    total_credits = models.PositiveIntegerField()

    def __str__(self):
        return self.program_name

class Semester(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('program', 'semester_number')
        ordering = ['program', 'semester_number']

    def __str__(self):
        return f"{self.program.program_name} - Semester {self.semester_number}"

class Course(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True)
    credits = models.PositiveSmallIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
