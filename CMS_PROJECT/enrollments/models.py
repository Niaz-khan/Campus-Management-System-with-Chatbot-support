from django.db import models
from students.models import Student
from courses.models import Course

class Enrollment(models.Model):
    """
    Model representing a student's enrollment in a course.
    Each student can enroll in multiple courses, and each course can have multiple students.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Each student enrolls only once per course
        ordering = ['student', 'course']

    def __str__(self):
        return f"{self.student.roll_number} ➔ {self.course.course_code}"
