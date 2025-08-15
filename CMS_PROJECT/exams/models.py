from django.db import models
from django.conf import settings
from decimal import Decimal

class Exam(models.Model):
    """Exam definition and configuration"""
    EXAM_TYPE_CHOICES = [
        ('midterm', 'Mid Term'),
        ('final', 'Final Term'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('lab', 'Laboratory'),
        ('viva', 'Viva Voce'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    semester = models.ForeignKey('courses.Semester', on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    pass_marks = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=200, blank=True)
    instructions = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-exam_date', '-start_time']
        unique_together = ('course', 'exam_type', 'semester')

    def __str__(self):
        return f"{self.title} - {self.course.course_code} ({self.exam_type})"

class ExamSchedule(models.Model):
    """Individual student exam schedule"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    is_eligible = models.BooleanField(default=True)
    attendance_status = models.CharField(
        max_length=15,
        choices=[
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('late', 'Late'),
            ('excused', 'Excused'),
        ],
        default='present'
    )
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['exam__exam_date', 'exam__start_time']

    def __str__(self):
        return f"{self.student} - {self.exam}"

class ExamResult(models.Model):
    """Individual student exam results"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)
    grade_points = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    remarks = models.TextField(blank=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-entered_at']

    def save(self, *args, **kwargs):
        # Auto-calculate percentage
        if self.exam.total_marks > 0:
            self.percentage = (self.marks_obtained / self.exam.total_marks) * 100
        
        # Auto-assign grade and grade points
        self.grade, self.grade_points = self.calculate_grade()
        
        super().save(*args, **kwargs)

    def calculate_grade(self):
        """Calculate grade based on percentage"""
        if self.percentage >= 90:
            return 'A+', Decimal('4.00')
        elif self.percentage >= 85:
            return 'A', Decimal('3.70')
        elif self.percentage >= 80:
            return 'A-', Decimal('3.50')
        elif self.percentage >= 75:
            return 'B+', Decimal('3.30')
        elif self.percentage >= 70:
            return 'B', Decimal('3.00')
        elif self.percentage >= 65:
            return 'B-', Decimal('2.70')
        elif self.percentage >= 60:
            return 'C+', Decimal('2.50')
        elif self.percentage >= 55:
            return 'C', Decimal('2.30')
        elif self.percentage >= 50:
            return 'C-', Decimal('2.00')
        elif self.percentage >= 45:
            return 'D+', Decimal('1.70')
        elif self.percentage >= 40:
            return 'D', Decimal('1.50')
        else:
            return 'F', Decimal('0.00')

    def __str__(self):
        return f"{self.student} - {self.exam} ({self.marks_obtained}/{self.exam.total_marks})"

class Grade(models.Model):
    """Grade scale configuration"""
    grade = models.CharField(max_length=2, unique=True)
    description = models.CharField(max_length=100)
    min_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    max_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    grade_points = models.DecimalField(max_digits=3, decimal_places=2)
    is_pass = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['grade_points']

    def __str__(self):
        return f"{self.grade} ({self.description})"

class Transcript(models.Model):
    """Student academic transcript"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    semester = models.ForeignKey('courses.Semester', on_delete=models.CASCADE)
    total_credits = models.PositiveIntegerField()
    earned_credits = models.PositiveIntegerField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    academic_status = models.CharField(
        max_length=20,
        choices=[
            ('good_standing', 'Good Standing'),
            ('probation', 'Academic Probation'),
            ('suspended', 'Suspended'),
            ('graduated', 'Graduated'),
        ],
        default='good_standing'
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('student', 'semester')
        ordering = ['-generated_at']

    def __str__(self):
        return f"Transcript - {self.student} - {self.semester}"

class ExamAttendance(models.Model):
    """Detailed exam attendance tracking"""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    is_late = models.BooleanField(default=False)
    late_minutes = models.PositiveIntegerField(default=0)
    supervisor_remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.student} - {self.exam} Attendance"
