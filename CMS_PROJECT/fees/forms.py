from django import forms
from .models import FeeStructure, FeeChallan, Payment, Scholarship

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = [
            'program', 'semester', 'tuition_fee', 'lab_fee', 
            'library_fee', 'examination_fee', 'other_fees', 
            'academic_year', 'is_active'
        ]
        widgets = {
            'program': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'tuition_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lab_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'library_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'examination_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'other_fees': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-2025'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FeeChallanForm(forms.ModelForm):
    class Meta:
        model = FeeChallan
        fields = [
            'student', 'fee_structure', 'challan_number', 
            'due_date', 'total_amount', 'remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'fee_structure': forms.Select(attrs={'class': 'form-control'}),
            'challan_number': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'challan', 'amount', 'payment_date', 'payment_method',
            'transaction_id', 'receipt_number', 'remarks'
        ]
        widgets = {
            'challan': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = [
            'student', 'scholarship_type', 'amount', 'percentage',
            'academic_year', 'semester', 'is_active', 'granted_date',
            'expiry_date', 'remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'scholarship_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-2025'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'granted_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FeeSummaryForm(forms.Form):
    """Form for generating fee summary reports"""
    REPORT_TYPE_CHOICES = [
        ('student', 'Student Summary'),
        ('department', 'Department Summary'),
        ('program', 'Program Summary'),
        ('overdue', 'Overdue Report'),
    ]
    
    report_type = forms.ChoiceField(
        choices=REPORT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    student_id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Student ID'})
    )
    department_id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Department ID'})
    )
    program_id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Program ID'})
    )
    from_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    to_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
