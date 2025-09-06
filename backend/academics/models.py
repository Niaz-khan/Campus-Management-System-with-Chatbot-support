from django.db import models

class Batch(models.Model):
    """
    Represents an academic batch (e.g., Fall 2025).
    """
    name = models.CharField(max_length=100, unique=True)  # e.g., Fall 2025
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    Represents a degree program within a batch (e.g., BS Computer Science).
    """
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=100)  # e.g., BSCS, BBA
    duration_years = models.PositiveIntegerField(default=4)
    total_semesters = models.PositiveIntegerField(default=8)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("batch", "name")  # Prevent duplicate program names within a batch

    def __str__(self):
        return f"{self.name} - {self.batch.name}"
