from django.db import models
from courses.models import Course
from students.models import Student

class Exam(models.Model):
    """
    Model representing an exam for a course.
    
    Attributes:
        course (ForeignKey): The course for which the exam is conducted.
        exam_type (str): The type of exam (mid-term, final-term, quiz).
        date (DateField): The date of the exam.
    """
    EXAM_TYPE_CHOICES = [
        ('mid', 'Mid-term'),
        ('final', 'Final-term'),
        ('quiz', 'Quiz'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.course.course_code} - {self.get_exam_type_display()}"

class ExamResult(models.Model):
    """
    Model representing the result of a student in an exam.
    Attributes:
        exam (ForeignKey): The exam for which the result is recorded.
        student (ForeignKey): The student who took the exam.
        marks_obtained (DecimalField): The marks obtained by the student in the exam.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('exam', 'student')
        ordering = ['exam', 'student']

    def __str__(self):
        return f"{self.student.roll_number} - {self.exam} - {self.marks_obtained}"
