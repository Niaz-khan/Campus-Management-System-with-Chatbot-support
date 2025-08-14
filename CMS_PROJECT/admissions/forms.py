from django import forms
from .models import AdmissionApplication

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'program', 'matric_marks', 'intermediate_marks', 'quota'
        ]
        widgets = {
            'program': forms.Select(attrs={'class': 'form-control'}),
            'matric_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'intermediate_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'quota': forms.TextInput(attrs={'class': 'form-control'}),
        }
