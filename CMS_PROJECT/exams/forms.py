from django import forms
from .models import Exam, ExamResult

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'exam_type', 'date']

class ExamResultForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['exam', 'student', 'marks_obtained']
        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'marks_obtained': 'Marks Obtained',
        }