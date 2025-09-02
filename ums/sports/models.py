from django.db import models
from django.conf import settings
from students.models import StudentProfile
from django.utils import timezone

class Facility(models.Model):
    FACILITY_TYPE_CHOICES = [
        ('SPORTS', 'Sports'),
        ('GYM', 'Gym'),
    ]
    name = models.CharField(max_length=150)
    facility_type = models.CharField(max_length=10, choices=FACILITY_TYPE_CHOICES, default='SPORTS')
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)  # e.g., max simultaneous users
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.facility_type})"


class GymMembership(models.Model):
    MEMBERSHIP_TYPE = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='gym_memberships')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='gym_memberships')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPE, default='MONTHLY')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'facility', 'start_date')

    def __str__(self):
        return f"{self.student.roll_no} - {self.facility.name} ({self.membership_type})"


class Equipment(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def can_issue(self, qty=1):
        return self.available_quantity >= qty


class EquipmentIssue(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='issues')
    issued_to = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='equipment_issues')
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    returned_at = models.DateField(null=True, blank=True)
    overdue_fine = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)  # optional
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipment.name} to {self.issued_to.roll_no}"


class Tournament(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date})"

    @property
    def registrations_count(self):
        return self.registrations.count()


class TournamentRegistration(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='tournament_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    fee_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('tournament', 'student')

    def __str__(self):
        return f"{self.student.roll_no} -> {self.tournament.name}"
