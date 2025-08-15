from django import forms
from .models import (
    Hostel, Room, Student, Staff, Maintenance, Visitor,
    Complaint, Payment, Notice
)

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = [
            'name', 'hostel_type', 'address', 'phone', 'email', 'capacity',
            'warden_name', 'warden_phone', 'warden_email', 'description',
            'amenities', 'rules', 'monthly_rent', 'security_deposit', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hostel_type': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'warden_name': forms.TextInput(attrs={'class': 'form-control'}),
            'warden_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'warden_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'hostel', 'room_number', 'room_type', 'floor', 'capacity',
            'monthly_rent', 'description', 'amenities', 'is_ac',
            'is_attached_bathroom', 'status'
        ]
        widgets = {
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_ac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_attached_bathroom': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'user', 'hostel', 'room', 'student_id', 'check_in_date',
            'check_out_date', 'monthly_rent', 'security_deposit',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'medical_conditions',
            'dietary_restrictions', 'is_active'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dietary_restrictions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'user', 'hostel', 'staff_type', 'employee_id', 'hire_date',
            'salary', 'phone', 'address', 'emergency_contact',
            'emergency_contact_phone', 'is_active'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'staff_type': forms.Select(attrs={'class': 'form-control'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'hostel', 'room', 'maintenance_type', 'priority', 'status',
            'title', 'description', 'scheduled_date', 'assigned_to',
            'estimated_cost', 'notes'
        ]
        widgets = {
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'hostel', 'student', 'visitor_name', 'visitor_type', 'phone',
            'id_proof_type', 'id_proof_number', 'purpose', 'notes'
        ]
        widgets = {
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'visitor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'visitor_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'id_proof_type': forms.TextInput(attrs={'class': 'form-control'}),
            'id_proof_number': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = [
            'hostel', 'student', 'complaint_type', 'priority', 'status',
            'title', 'description', 'assigned_to', 'resolution', 'is_anonymous'
        ]
        widgets = {
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
            'complaint_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'resolution': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'student', 'payment_type', 'amount', 'due_date', 'paid_date',
            'payment_method', 'status', 'reference_number', 'notes'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = [
            'hostel', 'title', 'content', 'notice_type', 'is_important',
            'is_active', 'expiry_date'
        ]
        widgets = {
            'hostel': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'notice_type': forms.Select(attrs={'class': 'form-control'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expiry_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

# Search and Filter Forms
class HostelSearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hostel name'}))
    hostel_type = forms.ChoiceField(choices=[('', 'All Types')] + Hostel.HOSTEL_TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    available_only = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Max monthly rent'}))

class RoomSearchForm(forms.Form):
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    room_type = forms.ChoiceField(choices=[('', 'All Types')] + Room.ROOM_TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    floor = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Floor number'}))
    available_only = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Max monthly rent'}))
    has_ac = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    has_attached_bathroom = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class StudentSearchForm(forms.Form):
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    is_active = forms.ChoiceField(choices=[('', 'All'), ('True', 'Active'), ('False', 'Inactive')], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    check_in_date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    check_in_date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

class MaintenanceSearchForm(forms.Form):
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    maintenance_type = forms.ChoiceField(choices=[('', 'All Types')] + Maintenance.MAINTENANCE_TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(choices=[('', 'All Priorities')] + Maintenance.PRIORITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Maintenance.STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    overdue_only = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class ComplaintSearchForm(forms.Form):
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    complaint_type = forms.ChoiceField(choices=[('', 'All Types')] + Complaint.COMPLAINT_TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(choices=[('', 'All Priorities')] + Complaint.PRIORITY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Complaint.STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    urgent_only = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class PaymentSearchForm(forms.Form):
    payment_type = forms.ChoiceField(choices=[('', 'All Types')] + Payment.PAYMENT_TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Payment.PAYMENT_STATUS_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    overdue_only = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

class NoticeSearchForm(forms.Form):
    hostel = forms.ModelChoiceField(queryset=Hostel.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    notice_type = forms.ChoiceField(choices=[('', 'All Types')] + Notice.NOTICE_TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    is_important = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    active_only = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
