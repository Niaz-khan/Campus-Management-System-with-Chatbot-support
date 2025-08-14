from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    """
    Form for enrolling a student in a course.
    Each student can enroll in multiple courses, and each course can have multiple students.
    """
    class Meta:
        """        
        Model representing a student's enrollment in a course.
        """
        model = Enrollment
        fields = ['student', 'course']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student': 'Student',
            'course': 'Course',
        }