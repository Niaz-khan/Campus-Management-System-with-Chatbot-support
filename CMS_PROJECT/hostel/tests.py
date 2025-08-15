from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, time, datetime, timedelta
from django.utils import timezone

from .models import (
    Hostel, Room, Student, Staff, Maintenance, Visitor,
    Complaint, Payment, Notice
)

User = get_user_model()

class HostelModelTest(TestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100,
            monthly_rent=Decimal('500.00'),
            security_deposit=Decimal('1000.00')
        )

    def test_hostel_creation(self):
        self.assertEqual(self.hostel.name, 'Test Hostel')
        self.assertEqual(self.hostel.hostel_type, 'male')
        self.assertEqual(self.hostel.capacity, 100)
        self.assertEqual(self.hostel.occupied, 0)
        self.assertEqual(self.hostel.is_active, True)

    def test_available_capacity_property(self):
        self.assertEqual(self.hostel.available_capacity, 100)
        self.hostel.occupied = 50
        self.hostel.save()
        self.assertEqual(self.hostel.available_capacity, 50)

    def test_occupancy_rate_property(self):
        self.assertEqual(self.hostel.occupancy_rate, 0)
        self.hostel.occupied = 50
        self.hostel.save()
        self.assertEqual(self.hostel.occupancy_rate, 50.0)

    def test_hostel_string_representation(self):
        self.assertEqual(str(self.hostel), 'Test Hostel')

class RoomModelTest(TestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100,
            monthly_rent=Decimal('500.00')
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number='101',
            room_type='double',
            floor=1,
            capacity=2
        )

    def test_room_creation(self):
        self.assertEqual(self.room.hostel, self.hostel)
        self.assertEqual(self.room.room_number, '101')
        self.assertEqual(self.room.room_type, 'double')
        self.assertEqual(self.room.floor, 1)
        self.assertEqual(self.room.capacity, 2)
        self.assertEqual(self.room.occupied, 0)
        self.assertEqual(self.room.status, 'available')

    def test_available_beds_property(self):
        self.assertEqual(self.room.available_beds, 2)
        self.room.occupied = 1
        self.room.save()
        self.assertEqual(self.room.available_beds, 1)

    def test_is_full_property(self):
        self.assertFalse(self.room.is_full)
        self.room.occupied = 2
        self.room.save()
        self.assertTrue(self.room.is_full)

    def test_room_string_representation(self):
        self.assertEqual(str(self.room), 'Test Hostel - Room 101')

    def test_room_unique_constraint(self):
        with self.assertRaises(Exception):
            Room.objects.create(
                hostel=self.hostel,
                room_number='101',
                room_type='single',
                floor=1,
                capacity=1
            )

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100,
            monthly_rent=Decimal('500.00')
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number='101',
            room_type='double',
            floor=1,
            capacity=2
        )
        self.student = Student.objects.create(
            user=self.user,
            hostel=self.hostel,
            room=self.room,
            student_id='ST001',
            check_in_date=date.today(),
            monthly_rent=Decimal('500.00'),
            security_deposit=Decimal('1000.00'),
            emergency_contact_name='John Doe',
            emergency_contact_phone='1234567890',
            emergency_contact_relationship='Father'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.user, self.user)
        self.assertEqual(self.student.hostel, self.hostel)
        self.assertEqual(self.student.room, self.room)
        self.assertEqual(self.student.student_id, 'ST001')
        self.assertEqual(self.student.is_active, True)

    def test_student_save_updates_room_and_hostel_occupancy(self):
        self.room.refresh_from_db()
        self.hostel.refresh_from_db()
        self.assertEqual(self.room.occupied, 1)
        self.assertEqual(self.hostel.occupied, 1)

    def test_student_string_representation(self):
        self.assertEqual(str(self.student), f"{self.user.get_full_name()} - {self.hostel.name}")

class StaffModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststaff',
            email='staff@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100
        )
        self.staff = Staff.objects.create(
            user=self.user,
            hostel=self.hostel,
            staff_type='warden',
            employee_id='EMP001',
            hire_date=date.today(),
            salary=Decimal('3000.00'),
            phone='1234567890',
            address='456 Staff Street',
            emergency_contact='Jane Doe',
            emergency_contact_phone='0987654321'
        )

    def test_staff_creation(self):
        self.assertEqual(self.staff.user, self.user)
        self.assertEqual(self.staff.hostel, self.hostel)
        self.assertEqual(self.staff.staff_type, 'warden')
        self.assertEqual(self.staff.employee_id, 'EMP001')
        self.assertEqual(self.staff.is_active, True)

    def test_staff_string_representation(self):
        self.assertEqual(str(self.staff), f"{self.user.get_full_name()} - Warden")

class MaintenanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number='101',
            room_type='double',
            floor=1,
            capacity=2
        )
        self.maintenance = Maintenance.objects.create(
            hostel=self.hostel,
            room=self.room,
            reported_by=self.user,
            maintenance_type='electrical',
            priority='high',
            title='Broken Light Switch',
            description='Light switch in room 101 is not working'
        )

    def test_maintenance_creation(self):
        self.assertEqual(self.maintenance.hostel, self.hostel)
        self.assertEqual(self.maintenance.room, self.room)
        self.assertEqual(self.maintenance.reported_by, self.user)
        self.assertEqual(self.maintenance.maintenance_type, 'electrical')
        self.assertEqual(self.maintenance.priority, 'high')
        self.assertEqual(self.maintenance.status, 'pending')

    def test_maintenance_string_representation(self):
        self.assertEqual(str(self.maintenance), f"Broken Light Switch - {self.hostel.name}")

    def test_is_overdue_property(self):
        self.assertFalse(self.maintenance.is_overdue)
        self.maintenance.scheduled_date = timezone.now() - timedelta(days=1)
        self.maintenance.save()
        self.assertTrue(self.maintenance.is_overdue)

    def test_days_overdue_property(self):
        self.assertEqual(self.maintenance.days_overdue, 0)
        self.maintenance.scheduled_date = timezone.now() - timedelta(days=3)
        self.maintenance.save()
        self.assertEqual(self.maintenance.days_overdue, 3)

class VisitorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100
        )
        self.student = Student.objects.create(
            user=self.user,
            hostel=self.hostel,
            student_id='ST001',
            check_in_date=date.today(),
            monthly_rent=Decimal('500.00'),
            security_deposit=Decimal('1000.00'),
            emergency_contact_name='John Doe',
            emergency_contact_phone='1234567890',
            emergency_contact_relationship='Father'
        )
        self.visitor = Visitor.objects.create(
            hostel=self.hostel,
            student=self.student,
            visitor_name='Jane Doe',
            visitor_type='family',
            phone='1234567890',
            id_proof_type='Passport',
            id_proof_number='P123456',
            purpose='Family visit'
        )

    def test_visitor_creation(self):
        self.assertEqual(self.visitor.hostel, self.hostel)
        self.assertEqual(self.visitor.student, self.student)
        self.assertEqual(self.visitor.visitor_name, 'Jane Doe')
        self.assertEqual(self.visitor.visitor_type, 'family')
        self.assertEqual(self.visitor.is_inside, True)

    def test_visitor_string_representation(self):
        self.assertEqual(str(self.visitor), f"Jane Doe visiting {self.student.user.get_full_name()}")

    def test_visitor_duration_property(self):
        self.assertIsNotNone(self.visitor.duration)

class ComplaintModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100
        )
        self.student = Student.objects.create(
            user=self.user,
            hostel=self.hostel,
            student_id='ST001',
            check_in_date=date.today(),
            monthly_rent=Decimal('500.00'),
            security_deposit=Decimal('1000.00'),
            emergency_contact_name='John Doe',
            emergency_contact_phone='1234567890',
            emergency_contact_relationship='Father'
        )
        self.complaint = Complaint.objects.create(
            hostel=self.hostel,
            student=self.student,
            complaint_type='noise',
            priority='medium',
            title='Noisy Neighbors',
            description='Neighbors are making too much noise at night'
        )

    def test_complaint_creation(self):
        self.assertEqual(self.complaint.hostel, self.hostel)
        self.assertEqual(self.complaint.student, self.student)
        self.assertEqual(self.complaint.complaint_type, 'noise')
        self.assertEqual(self.complaint.priority, 'medium')
        self.assertEqual(self.complaint.status, 'open')
        self.assertEqual(self.complaint.is_anonymous, False)

    def test_complaint_string_representation(self):
        self.assertEqual(str(self.complaint), f"Noisy Neighbors - {self.student.user.get_full_name()}")

class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100
        )
        self.student = Student.objects.create(
            user=self.user,
            hostel=self.hostel,
            student_id='ST001',
            check_in_date=date.today(),
            monthly_rent=Decimal('500.00'),
            security_deposit=Decimal('1000.00'),
            emergency_contact_name='John Doe',
            emergency_contact_phone='1234567890',
            emergency_contact_relationship='Father'
        )
        self.payment = Payment.objects.create(
            student=self.student,
            payment_type='rent',
            amount=Decimal('500.00'),
            due_date=date.today() + timedelta(days=30)
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.student, self.student)
        self.assertEqual(self.payment.payment_type, 'rent')
        self.assertEqual(self.payment.amount, Decimal('500.00'))
        self.assertEqual(self.payment.status, 'pending')

    def test_payment_string_representation(self):
        self.assertEqual(str(self.payment), f"{self.student.user.get_full_name()} - Monthly Rent - $500.00")

    def test_is_overdue_property(self):
        self.assertFalse(self.payment.is_overdue)
        self.payment.due_date = date.today() - timedelta(days=1)
        self.payment.save()
        self.assertTrue(self.payment.is_overdue)

    def test_days_overdue_property(self):
        self.assertEqual(self.payment.days_overdue, 0)
        self.payment.due_date = date.today() - timedelta(days=5)
        self.payment.save()
        self.assertEqual(self.payment.days_overdue, 5)

class NoticeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='user@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100
        )
        self.notice = Notice.objects.create(
            hostel=self.hostel,
            title='Important Notice',
            content='This is an important notice for all students',
            notice_type='general',
            is_important=True,
            published_by=self.user
        )

    def test_notice_creation(self):
        self.assertEqual(self.notice.hostel, self.hostel)
        self.assertEqual(self.notice.title, 'Important Notice')
        self.assertEqual(self.notice.content, 'This is an important notice for all students')
        self.assertEqual(self.notice.notice_type, 'general')
        self.assertEqual(self.notice.is_important, True)
        self.assertEqual(self.notice.is_active, True)

    def test_notice_string_representation(self):
        self.assertEqual(str(self.notice), f"Important Notice - {self.hostel.name}")

    def test_is_expired_property(self):
        self.assertFalse(self.notice.is_expired)
        self.notice.expiry_date = timezone.now() - timedelta(days=1)
        self.notice.save()
        self.assertTrue(self.notice.is_expired)

class HostelModelIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            hostel_type='male',
            address='123 Test Street',
            capacity=100,
            monthly_rent=Decimal('500.00')
        )
        self.room = Room.objects.create(
            hostel=self.hostel,
            room_number='101',
            room_type='double',
            floor=1,
            capacity=2
        )

    def test_complete_student_lifecycle(self):
        # Create student
        student = Student.objects.create(
            user=self.user,
            hostel=self.hostel,
            room=self.room,
            student_id='ST001',
            check_in_date=date.today(),
            monthly_rent=Decimal('500.00'),
            security_deposit=Decimal('1000.00'),
            emergency_contact_name='John Doe',
            emergency_contact_phone='1234567890',
            emergency_contact_relationship='Father'
        )
        
        # Check room and hostel occupancy
        self.room.refresh_from_db()
        self.hostel.refresh_from_db()
        self.assertEqual(self.room.occupied, 1)
        self.assertEqual(self.hostel.occupied, 1)
        
        # Check out student
        student.is_active = False
        student.check_out_date = date.today()
        student.save()
        
        # Check room and hostel occupancy after check out
        self.room.refresh_from_db()
        self.hostel.refresh_from_db()
        self.assertEqual(self.room.occupied, 0)
        self.assertEqual(self.hostel.occupied, 0)

    def test_room_rent_inheritance(self):
        # Room should inherit rent from hostel if not specified
        room = Room.objects.create(
            hostel=self.hostel,
            room_number='102',
            room_type='single',
            floor=1,
            capacity=1
        )
        self.assertEqual(room.monthly_rent, self.hostel.monthly_rent)
        
        # Custom room rent should override hostel rent
        custom_room = Room.objects.create(
            hostel=self.hostel,
            room_number='103',
            room_type='single',
            floor=1,
            capacity=1,
            monthly_rent=Decimal('600.00')
        )
        self.assertEqual(custom_room.monthly_rent, Decimal('600.00'))
