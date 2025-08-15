from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Department, Faculty

User = get_user_model()

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            description='Computer Science Department'
        )
    
    def test_department_creation(self):
        self.assertEqual(self.department.name, 'Computer Science')
        self.assertEqual(self.department.code, 'CS')
        self.assertEqual(str(self.department), 'CS - Computer Science')

class FacultyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testfaculty',
            email='faculty@test.com',
            password='testpass123'
        )
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
        self.faculty = Faculty.objects.create(
            user=self.user,
            employee_id='CS001',
            department=self.department,
            designation='assistant_professor',
            qualification='PhD Computer Science',
            joining_date='2023-01-01'
        )
    
    def test_faculty_creation(self):
        self.assertEqual(self.faculty.employee_id, 'CS001')
        self.assertEqual(self.faculty.designation, 'assistant_professor')
        self.assertEqual(self.faculty.status, 'active')
        self.assertEqual(str(self.faculty), 'CS001 - testfaculty (assistant_professor)')
