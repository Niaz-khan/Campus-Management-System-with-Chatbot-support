from rest_framework import serializers
from .models import FeeStructure, FeeChallan, Payment, Scholarship

class FeeStructureSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source='program.program_name', read_only=True)
    semester_info = serializers.CharField(source='semester.__str__', read_only=True)

    class Meta:
        model = FeeStructure
        fields = [
            'id', 'program', 'program_name', 'semester', 'semester_info',
            'tuition_fee', 'lab_fee', 'library_fee', 'examination_fee',
            'other_fees', 'total_fee', 'academic_year', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['total_fee', 'created_at', 'updated_at']

class FeeChallanSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    fee_structure_info = serializers.CharField(source='fee_structure.__str__', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = FeeChallan
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'fee_structure',
            'fee_structure_info', 'challan_number', 'issue_date', 'due_date',
            'total_amount', 'paid_amount', 'remaining_amount', 'status',
            'status_display', 'remarks'
        ]
        read_only_fields = ['issue_date', 'remaining_amount']

class PaymentSerializer(serializers.ModelSerializer):
    challan_info = serializers.CharField(source='challan.__str__', read_only=True)
    student_name = serializers.CharField(source='challan.student.user.get_full_name', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    received_by_name = serializers.CharField(source='received_by.get_full_name', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'challan', 'challan_info', 'student_name', 'amount',
            'payment_date', 'payment_method', 'payment_method_display',
            'transaction_id', 'receipt_number', 'received_by', 'received_by_name',
            'remarks', 'created_at'
        ]
        read_only_fields = ['created_at']

class ScholarshipSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    scholarship_type_display = serializers.CharField(source='get_scholarship_type_display', read_only=True)
    semester_info = serializers.CharField(source='semester.__str__', read_only=True)

    class Meta:
        model = Scholarship
        fields = [
            'id', 'student', 'student_name', 'student_roll', 'scholarship_type',
            'scholarship_type_display', 'amount', 'percentage', 'academic_year',
            'semester', 'semester_info', 'is_active', 'granted_date',
            'expiry_date', 'remarks'
        ]

class FeeSummarySerializer(serializers.Serializer):
    """Serializer for student fee summary"""
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    total_fees = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_remaining = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_scholarships = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_remaining = serializers.DecimalField(max_digits=10, decimal_places=2)
    overdue_challans = serializers.IntegerField()
    pending_challans = serializers.IntegerField()
