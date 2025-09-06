from django.contrib import admin
from .models import FeeCategory, Invoice, Payment

@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_recurring")
    search_fields = ("name",)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("reference_number", "student", "amount", "due_date", "is_paid")
    list_filter = ("is_paid", "due_date", "category")
    search_fields = ("reference_number", "student__roll_no")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "method", "created_at")
    search_fields = ("invoice__reference_number",)
