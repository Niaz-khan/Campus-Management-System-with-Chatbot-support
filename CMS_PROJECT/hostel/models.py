from django.db import models
from django.conf import settings
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone

class Hostel(models.Model):
    HOSTEL_TYPE_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('mixed', 'Mixed'),
    ]
    
    name = models.CharField(max_length=200)
    hostel_type = models.CharField(max_length=10, choices=HOSTEL_TYPE_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    capacity = models.PositiveIntegerField(help_text="Total number of students that can be accommodated")
    occupied = models.PositiveIntegerField(default=0, help_text="Number of currently occupied beds")
    warden_name = models.CharField(max_length=100, blank=True)
    warden_phone = models.CharField(max_length=20, blank=True)
    warden_email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True, help_text="List of available amenities")
    rules = models.TextField(blank=True, help_text="Hostel rules and regulations")
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def available_capacity(self):
        return self.capacity - self.occupied
    
    @property
    def occupancy_rate(self):
        if self.capacity > 0:
            return (self.occupied / self.capacity) * 100
        return 0

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
        ('dormitory', 'Dormitory'),
    ]
    
    ROOM_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
        ('unavailable', 'Unavailable'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    floor = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(help_text="Number of students that can stay in this room")
    occupied = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default='available')
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True, help_text="Room-specific amenities")
    is_ac = models.BooleanField(default=False, help_text="Air conditioning available")
    is_attached_bathroom = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('hostel', 'room_number')
        ordering = ['hostel', 'floor', 'room_number']
    
    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"
    
    @property
    def available_beds(self):
        return self.capacity - self.occupied
    
    @property
    def is_full(self):
        return self.occupied >= self.capacity
    
    def save(self, *args, **kwargs):
        if not self.monthly_rent:
            self.monthly_rent = self.hostel.monthly_rent
        super().save(*args, **kwargs)

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hostel_student')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='students')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField(null=True, blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relationship = models.CharField(max_length=50)
    medical_conditions = models.TextField(blank=True)
    dietary_restrictions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-check_in_date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.hostel.name}"
    
    def save(self, *args, **kwargs):
        if self.room and self.is_active:
            self.room.occupied += 1
            self.room.save()
            self.hostel.occupied += 1
            self.hostel.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.room and self.is_active:
            self.room.occupied -= 1
            self.room.save()
            self.hostel.occupied -= 1
            self.hostel.save()
        super().delete(*args, **kwargs)

class Staff(models.Model):
    STAFF_TYPE_CHOICES = [
        ('warden', 'Warden'),
        ('caretaker', 'Caretaker'),
        ('cleaner', 'Cleaner'),
        ('security', 'Security Guard'),
        ('maintenance', 'Maintenance Staff'),
        ('cook', 'Cook'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hostel_staff')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='staff')
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES)
    employee_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['hostel', 'staff_type', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_staff_type_display()}"

class Maintenance(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('carpentry', 'Carpentry'),
        ('cleaning', 'Cleaning'),
        ('pest_control', 'Pest Control'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='maintenance_requests')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests', null=True, blank=True)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_maintenance')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_maintenance')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reported_date']
    
    def __str__(self):
        return f"{self.title} - {self.hostel.name}"
    
    @property
    def is_overdue(self):
        if self.scheduled_date and self.status == 'pending':
            return self.scheduled_date < timezone.now()
        return False
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (timezone.now() - self.scheduled_date).days
        return 0

class Visitor(models.Model):
    VISITOR_TYPE_CHOICES = [
        ('family', 'Family Member'),
        ('friend', 'Friend'),
        ('delivery', 'Delivery Person'),
        ('service', 'Service Provider'),
        ('other', 'Other'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='visitors')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='visitors')
    visitor_name = models.CharField(max_length=100)
    visitor_type = models.CharField(max_length=20, choices=VISITOR_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    id_proof_type = models.CharField(max_length=50)
    id_proof_number = models.CharField(max_length=50)
    purpose = models.TextField()
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    is_inside = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-check_in_time']
    
    def __str__(self):
        return f"{self.visitor_name} visiting {self.student.user.get_full_name()}"
    
    @property
    def duration(self):
        if self.check_out_time:
            return self.check_out_time - self.check_in_time
        return timezone.now() - self.check_in_time

class Complaint(models.Model):
    COMPLAINT_TYPE_CHOICES = [
        ('noise', 'Noise Complaint'),
        ('cleanliness', 'Cleanliness Issue'),
        ('maintenance', 'Maintenance Issue'),
        ('security', 'Security Concern'),
        ('food', 'Food Quality Issue'),
        ('roommate', 'Roommate Issue'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='complaints')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    title = models.CharField(max_length=200)
    description = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    resolution = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reported_date']
    
    def __str__(self):
        return f"{self.title} - {self.student.user.get_full_name()}"

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('rent', 'Monthly Rent'),
        ('security_deposit', 'Security Deposit'),
        ('fine', 'Fine'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
        ('check', 'Check'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_payment_type_display()} - ${self.amount}"
    
    @property
    def is_overdue(self):
        if self.status == 'pending':
            return self.due_date < date.today()
        return False
    
    @property
    def days_overdue(self):
        if self.is_overdue:
            return (date.today() - self.due_date).days
        return 0

class Notice(models.Model):
    NOTICE_TYPE_CHOICES = [
        ('general', 'General'),
        ('maintenance', 'Maintenance'),
        ('event', 'Event'),
        ('rule', 'Rule Update'),
        ('emergency', 'Emergency'),
        ('other', 'Other'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='notices')
    title = models.CharField(max_length=200)
    content = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPE_CHOICES, default='general')
    is_important = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='published_notices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return f"{self.title} - {self.hostel.name}"
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False
