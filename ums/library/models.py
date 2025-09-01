from django.db import models
from django.conf import settings
from students.models import StudentProfile

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('SCIENCE', 'Science'),
        ('ENGINEERING', 'Engineering'),
        ('LITERATURE', 'Literature'),
        ('ARTS', 'Arts'),
        ('OTHERS', 'Others'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='OTHERS')
    isbn = models.CharField(max_length=20, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role__in': ['FACULTY', 'ADMIN']},
        related_name="added_books"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookBorrow(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "book", "borrowed_at")

    def __str__(self):
        return f"{self.student.roll_no} borrowed {self.book.title}"


class BookFine(models.Model):
    borrow_record = models.OneToOneField(BookBorrow, on_delete=models.CASCADE, related_name="fine")
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Fine for {self.borrow_record.book.title}: {self.fine_amount}"
