from django import forms
from .models import Exam, ExamSchedule, ExamResult, Grade, Transcript, ExamAttendance

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'title', 'exam_type', 'course', 'semester', 'total_marks', 'pass_marks',
            'duration_minutes', 'exam_date', 'start_time', 'end_time', 'venue',
            'instructions', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ExamScheduleForm(forms.ModelForm):
    class Meta:
        model = ExamSchedule
        fields = [
            'student', 'exam', 'is_eligible', 'attendance_status', 'remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'is_eligible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'attendance_status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = [
            'student', 'exam', 'marks_obtained', 'remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            'grade', 'description', 'min_percentage', 'max_percentage',
            'grade_points', 'is_pass', 'remarks'
        ]
        widgets = {
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'min_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'grade_points': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_pass': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TranscriptForm(forms.ModelForm):
    class Meta:
        model = Transcript
        fields = [
            'student', 'semester', 'total_credits', 'earned_credits',
            'gpa', 'cgpa', 'academic_status'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'total_credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'earned_credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'academic_status': forms.Select(attrs={'class': 'form-control'}),
        }

class ExamAttendanceForm(forms.ModelForm):
    class Meta:
        model = ExamAttendance
        fields = [
            'student', 'exam', 'check_in_time', 'check_out_time',
            'is_late', 'late_minutes', 'supervisor_remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'exam': forms.Select(attrs={'class': 'form-control'}),
            'check_in_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'check_out_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_late': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'late_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'supervisor_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ExamSearchForm(forms.Form):
    """Form for searching exams"""
    SEARCH_TYPE_CHOICES = [
        ('title', 'Exam Title'),
        ('course', 'Course'),
        ('exam_type', 'Exam Type'),
        ('date_range', 'Date Range'),
        ('status', 'Status'),
    ]
    
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search query'})
    )
    course = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    exam_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Exam.EXAM_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Exam.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        from courses.models import Course
        self.fields['course'].queryset = Course.objects.all()

class ExamResultSearchForm(forms.Form):
    """Form for searching exam results"""
    student = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    exam = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    grade = forms.ChoiceField(
        choices=[('', 'All Grades')] + [
            ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
            ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
            ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
            ('D+', 'D+'), ('D', 'D'), ('F', 'F'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_percentage = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Min %'})
    )
    max_percentage = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Max %'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports
        from students.models import Student
        self.fields['student'].queryset = Student.objects.all()
        self.fields['exam'].queryset = Exam.objects.all()