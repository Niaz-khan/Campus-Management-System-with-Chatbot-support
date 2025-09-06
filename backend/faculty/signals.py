from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import FacultyProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_faculty_profile(sender, instance, created, **kwargs):
    if created and instance.role == "FACULTY":
        FacultyProfile.objects.create(user=instance, designation="Lecturer")
