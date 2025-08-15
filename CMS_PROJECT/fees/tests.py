from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta

from .models import FeeStructure, FeeChallan, Payment, Scholarship

User = get_user_model()

class FeeStructureModelTest(TestCase):
    def setUp(self):
        # Create test program and semester (you'll need to import these from other apps)
        from courses.models import Program, Semester
        
        self.program = Program.objects.create(
            program_name='BSCS',
            department='Computer Science',
            duration_years=4,
            total_credits=130
        )
        
        self.semester = Semester.objects.create(
            program=self.program,
            semester_number=1,
            year=2024,
            term='Fall'
        )

    def test_fee_structure_creation(self):
        fee_structure = FeeStructure.objects.create(
            program=self.program,
            semester=self.semester,
            tuition_fee=Decimal('50000.00'),
            lab_fee=Decimal('5000.00'),
            library_fee=Decimal('2000.00'),
            examination_fee=Decimal('3000.00'),
            other_fees=Decimal('1000.00'),
            academic_year='2024-2025'
        )
        
        self.assertEqual(fee_structure.total_fee, Decimal('65000.00'))
        self.assertEqual(str(fee_structure), f"BSCS - Sem 1 (2024-2025)")

    def test_fee_structure_auto_calculation(self):
        fee_structure = FeeStructure.objects.create(
            program=self.program,
            semester=self.semester,
            tuition_fee=Decimal('40000.00'),
            lab_fee=Decimal('4000.00'),
            library_fee=Decimal('1500.00'),
            examination_fee=Decimal('2500.00'),
            other_fees=Decimal('500.00'),
            academic_year='2024-2025'
        )
        
        # Test auto-calculation
        self.assertEqual(fee_structure.total_fee, Decimal('50000.00'))

class FeeChallanModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.program = Program.objects.create(
            program_name='BSCS',
            department='Computer Science',
            duration_years=4,
            total_credits=130
        )
        
        self.semester = Semester.objects.create(
            program=self.program,
            semester_number=1,
            year=2024,
            term='Fall'
        )
        
        self.student = Student.objects.create(
            user=self.user,
            roll_number='BSCS2024001',
            program=self.program,
            batch='BSCS-2024'
        )
        
        self.fee_structure = FeeStructure.objects.create(
            program=self.program,
            semester=self.semester,
            tuition_fee=Decimal('50000.00'),
            lab_fee=Decimal('5000.00'),
            library_fee=Decimal('2000.00'),
            examination_fee=Decimal('3000.00'),
            other_fees=Decimal('1000.00'),
            academic_year='2024-2025'
        )

    def test_challan_creation(self):
        challan = FeeChallan.objects.create(
            student=self.student,
            fee_structure=self.fee_structure,
            challan_number='CH001',
            due_date=date.today() + timedelta(days=30),
            total_amount=Decimal('65000.00')
        )
        
        self.assertEqual(challan.remaining_amount, Decimal('65000.00'))
        self.assertEqual(challan.status, 'pending')
        self.assertEqual(str(challan), f"Challan CH001 - {self.student}")

    def test_challan_auto_calculation(self):
        challan = FeeChallan.objects.create(
            student=self.student,
            fee_structure=self.fee_structure,
            challan_number='CH002',
            due_date=date.today() + timedelta(days=30),
            total_amount=Decimal('65000.00')
        )
        
        # Test auto-calculation of remaining amount
        challan.paid_amount = Decimal('30000.00')
        challan.save()
        
        self.assertEqual(challan.remaining_amount, Decimal('35000.00'))

class PaymentModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True
        )
        
        self.program = Program.objects.create(
            program_name='BSCS',
            department='Computer Science',
            duration_years=4,
            total_credits=130
        )
        
        self.semester = Semester.objects.create(
            program=self.program,
            semester_number=1,
            year=2024,
            term='Fall'
        )
        
        self.student = Student.objects.create(
            user=self.user,
            roll_number='BSCS2024001',
            program=self.program,
            batch='BSCS-2024'
        )
        
        self.fee_structure = FeeStructure.objects.create(
            program=self.program,
            semester=self.semester,
            tuition_fee=Decimal('50000.00'),
            lab_fee=Decimal('5000.00'),
            library_fee=Decimal('2000.00'),
            examination_fee=Decimal('3000.00'),
            other_fees=Decimal('1000.00'),
            academic_year='2024-2025'
        )
        
        self.challan = FeeChallan.objects.create(
            student=self.student,
            fee_structure=self.fee_structure,
            challan_number='CH001',
            due_date=date.today() + timedelta(days=30),
            total_amount=Decimal('65000.00')
        )

    def test_payment_creation(self):
        payment = Payment.objects.create(
            challan=self.challan,
            amount=Decimal('30000.00'),
            payment_date=date.today(),
            payment_method='bank_transfer',
            receipt_number='R001',
            received_by=self.admin_user
        )
        
        self.assertEqual(str(payment), f"Payment R001 - {self.challan}")

class ScholarshipModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.program = Program.objects.create(
            program_name='BSCS',
            department='Computer Science',
            duration_years=4,
            total_credits=130
        )
        
        self.semester = Semester.objects.create(
            program=self.program,
            semester_number=1,
            year=2024,
            term='Fall'
        )
        
        self.student = Student.objects.create(
            user=self.user,
            roll_number='BSCS2024001',
            program=self.program,
            batch='BSCS-2024'
        )

    def test_scholarship_creation(self):
        scholarship = Scholarship.objects.create(
            student=self.student,
            scholarship_type='merit',
            amount=Decimal('10000.00'),
            percentage=Decimal('15.00'),
            academic_year='2024-2025',
            semester=self.semester,
            granted_date=date.today()
        )
        
        self.assertEqual(str(scholarship), f"merit - {self.student} (2024-2025)")
        self.assertTrue(scholarship.is_active)
