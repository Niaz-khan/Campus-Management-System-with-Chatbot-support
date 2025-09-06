from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Grade
from .services import calculate_student_cgpa

@receiver([post_save, post_delete], sender=Grade)
def update_student_cgpa(sender, instance, **kwargs):
    student = instance.enrollment.student
    cgpa, credits = calculate_student_cgpa(student)
    student.cgpa = cgpa
    student.credits_completed = credits
    student.save(update_fields=['cgpa', 'credits_completed'])
