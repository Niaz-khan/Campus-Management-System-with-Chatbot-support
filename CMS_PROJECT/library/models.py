from django.db import models
from django.conf import settings
from decimal import Decimal
from datetime import date, timedelta

class Author(models.Model):
    """Book author information"""
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    """Book category/classification"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Publisher(models.Model):
    """Book publisher information"""
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    """Book information and metadata"""
    BOOK_TYPE_CHOICES = [
        ('textbook', 'Textbook'),
        ('reference', 'Reference'),
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('magazine', 'Magazine'),
        ('journal', 'Journal'),
        ('newspaper', 'Newspaper'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('limited', 'Limited Availability'),
        ('unavailable', 'Unavailable'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=300, blank=True)
    isbn = models.CharField(max_length=20, unique=True, blank=True)
    isbn13 = models.CharField(max_length=20, unique=True, blank=True)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPE_CHOICES, default='textbook')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=100, blank=True, help_text='Shelf/rack location')
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-update available copies if total copies changed
        if self.pk:
            old_instance = Book.objects.get(pk=self.pk)
            if old_instance.total_copies != self.total_copies:
                difference = self.total_copies - old_instance.total_copies
                self.available_copies += difference
        super().save(*args, **kwargs)

class BookCopy(models.Model):
    """Individual copy of a book"""
    COPY_STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
    copy_number = models.CharField(max_length=20, unique=True)
    acquisition_date = models.DateField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    condition = models.CharField(max_length=20, choices=COPY_STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['copy_number']
        verbose_name_plural = 'Book copies'

    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"

class Borrowing(models.Model):
    """Book borrowing record"""
    BORROW_STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
        ('damaged', 'Damaged'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='borrowings')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='borrowings')
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=BORROW_STATUS_CHOICES, default='active')
    renewed_count = models.PositiveIntegerField(default=0)
    max_renewals = models.PositiveIntegerField(default=2)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='issued_borrowings')
    returned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name='returned_borrowings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-borrowed_date']

    def __str__(self):
        return f"{self.student} - {self.book_copy.book.title}"

    def save(self, *args, **kwargs):
        # Auto-calculate due date if not set
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)  # Default 2 weeks
        
        # Update book copy status
        if self.status == 'active':
            self.book_copy.condition = 'borrowed'
        elif self.status == 'returned':
            self.book_copy.condition = 'available'
        
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.status == 'active' and self.due_date < date.today():
            return True
        return False

    @property
    def days_overdue(self):
        if self.is_overdue:
            return (date.today() - self.due_date).days
        return 0

class Reservation(models.Model):
    """Book reservation system"""
    RESERVATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-reservation_date']
        unique_together = ['student', 'book', 'status']

    def __str__(self):
        return f"{self.student} - {self.book.title}"

    def save(self, *args, **kwargs):
        # Auto-set expiry date if not set (24 hours from reservation)
        if not self.expiry_date:
            from django.utils import timezone
            self.expiry_date = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

class Fine(models.Model):
    """Fine management for overdue/lost books"""
    FINE_TYPE_CHOICES = [
        ('overdue', 'Overdue'),
        ('lost', 'Lost Book'),
        ('damaged', 'Damaged Book'),
        ('other', 'Other'),
    ]

    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE, related_name='fines')
    fine_type = models.CharField(max_length=20, choices=FINE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Fine {self.id} - {self.borrowing.student} - {self.amount}"

class LibraryCard(models.Model):
    """Student library card management"""
    CARD_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    student = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='library_card')
    card_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=CARD_STATUS_CHOICES, default='active')
    max_books = models.PositiveIntegerField(default=5)
    max_days = models.PositiveIntegerField(default=14)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"Card {self.card_number} - {self.student}"

    def save(self, *args, **kwargs):
        # Auto-set expiry date if not set (1 year from issue)
        if not self.expiry_date:
            self.expiry_date = date.today() + timedelta(days=365)
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.expiry_date < date.today()

    @property
    def days_until_expiry(self):
        return (self.expiry_date - date.today()).days
