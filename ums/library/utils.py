from datetime import date
from decimal import Decimal

def calculate_overdue_fine(invoice_amount, percent_per_day, overdue_days):
    # helper if needed
    return (Decimal(invoice_amount) * (Decimal(percent_per_day) / Decimal('100')) * Decimal(overdue_days))
