from rest_framework import serializers
from .models import FeeCategory, Invoice, Payment

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = ['id', 'name', 'description', 'is_recurring']


class InvoiceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    calculated_fine = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'student', 'student_name', 'category', 'amount',
            'due_date', 'is_paid', 'paid_at', 'reference_number',
            'fine_percentage_per_day', 'fine_amount', 'calculated_fine',
            'fine_applied', 'notes', 'created_at'
        ]
        read_only_fields = [
            'is_paid', 'paid_at', 'created_at', 'fine_amount', 'fine_applied'
        ]

    def get_calculated_fine(self, obj):
        return obj.calculate_fine()



class PaymentSerializer(serializers.ModelSerializer):
    invoice_ref = serializers.CharField(source='invoice.reference_number', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'invoice_ref', 'amount', 'method',
            'paid_by', 'transaction_id', 'created_at'
        ]
        read_only_fields = ['paid_by', 'created_at']
