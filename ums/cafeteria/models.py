from django.db import models
from django.conf import settings
from students.models import StudentProfile
from django.utils import timezone

class MealPlan(models.Model):
    MEAL_TYPE_CHOICES = [
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
    ]
    name = models.CharField(max_length=150)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    menu = models.TextField(help_text="Menu details")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.meal_type})"


class MessSubscription(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="mess_subscriptions")
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="subscriptions")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subscribed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'meal_plan', 'start_date')

    def __str__(self):
        return f"{self.student.roll_no} – {self.meal_plan.name}"


class MealAttendance(models.Model):
    subscription = models.ForeignKey(MessSubscription, on_delete=models.CASCADE, related_name="meal_attendance")
    date = models.DateField()
    attended = models.BooleanField(default=False)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, limit_choices_to={'role': 'FACULTY'}
    )
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscription', 'date')

    def __str__(self):
        return f"{self.subscription.student.roll_no} – {self.date} ({'Present' if self.attended else 'Absent'})"
