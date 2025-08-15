from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, time, datetime, timedelta

from .models import Exam, ExamSchedule, ExamResult, Grade, Transcript, ExamAttendance

User = get_user_model()

class ExamModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Course, Program, Semester
        
        self.user = User.objects.create_user(
            username='testfaculty',
            email='faculty@test.com',
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
        
        self.course = Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Programming',
            credits=3,
            program=self.program,
            semester=self.semester
        )

    def test_exam_creation(self):
        exam = Exam.objects.create(
            title='Mid Term Exam',
            exam_type='midterm',
            course=self.course,
            semester=self.semester,
            total_marks=100,
            pass_marks=40,
            duration_minutes=120,
            exam_date=date(2024, 12, 15),
            start_time=time(9, 0),
            end_time=time(11, 0),
            venue='Room 101',
            instructions='Bring calculator',
            created_by=self.user
        )
        
        self.assertEqual(exam.title, 'Mid Term Exam')
        self.assertEqual(exam.exam_type, 'midterm')
        self.assertEqual(exam.status, 'draft')
        self.assertEqual(str(exam), f"Mid Term Exam - CS101 (midterm)")

    def test_exam_unique_constraint(self):
        # Create first exam
        Exam.objects.create(
            title='Mid Term Exam',
            exam_type='midterm',
            course=self.course,
            semester=self.semester,
            total_marks=100,
            pass_marks=40,
            duration_minutes=120,
            exam_date=date(2024, 12, 15),
            start_time=time(9, 0),
            end_time=time(11, 0),
            created_by=self.user
        )
        
        # Try to create another exam with same course, type, and semester
        with self.assertRaises(Exception):
            Exam.objects.create(
                title='Another Mid Term',
                exam_type='midterm',
                course=self.course,
                semester=self.semester,
                total_marks=100,
                pass_marks=40,
                duration_minutes=120,
                exam_date=date(2024, 12, 20),
                start_time=time(9, 0),
                end_time=time(11, 0),
                created_by=self.user
            )

class ExamScheduleModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Course, Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.faculty_user = User.objects.create_user(
            username='testfaculty',
            email='faculty@test.com',
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
        
        self.course = Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Programming',
            credits=3,
            program=self.program,
            semester=self.semester
        )
        
        self.student = Student.objects.create(
            user=self.user,
            roll_number='BSCS2024001',
            program=self.program,
            batch='BSCS-2024'
        )
        
        self.exam = Exam.objects.create(
            title='Mid Term Exam',
            exam_type='midterm',
            course=self.course,
            semester=self.semester,
            total_marks=100,
            pass_marks=40,
            duration_minutes=120,
            exam_date=date(2024, 12, 15),
            start_time=time(9, 0),
            end_time=time(11, 0),
            created_by=self.faculty_user
        )

    def test_exam_schedule_creation(self):
        schedule = ExamSchedule.objects.create(
            student=self.student,
            exam=self.exam,
            is_eligible=True,
            attendance_status='present'
        )
        
        self.assertEqual(schedule.student, self.student)
        self.assertEqual(schedule.exam, self.exam)
        self.assertTrue(schedule.is_eligible)
        self.assertEqual(schedule.attendance_status, 'present')
        self.assertEqual(str(schedule), f"{self.student} - {self.exam}")

class ExamResultModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Course, Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.faculty_user = User.objects.create_user(
            username='testfaculty',
            email='faculty@test.com',
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
        
        self.course = Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Programming',
            credits=3,
            program=self.program,
            semester=self.semester
        )
        
        self.student = Student.objects.create(
            user=self.user,
            roll_number='BSCS2024001',
            program=self.program,
            batch='BSCS-2024'
        )
        
        self.exam = Exam.objects.create(
            title='Mid Term Exam',
            exam_type='midterm',
            course=self.course,
            semester=self.semester,
            total_marks=100,
            pass_marks=40,
            duration_minutes=120,
            exam_date=date(2024, 12, 15),
            start_time=time(9, 0),
            end_time=time(11, 0),
            created_by=self.faculty_user
        )

    def test_exam_result_creation(self):
        result = ExamResult.objects.create(
            student=self.student,
            exam=self.exam,
            marks_obtained=Decimal('85.50'),
            entered_by=self.faculty_user
        )
        
        # Test auto-calculated fields
        self.assertEqual(result.percentage, Decimal('85.50'))
        self.assertEqual(result.grade, 'A')
        self.assertEqual(result.grade_points, Decimal('3.70'))
        self.assertEqual(str(result), f"{self.student} - {self.exam} (85.50/100)")

    def test_grade_calculation(self):
        # Test different grade ranges
        test_cases = [
            (95, 'A+', Decimal('4.00')),
            (87, 'A', Decimal('3.70')),
            (82, 'A-', Decimal('3.50')),
            (78, 'B+', Decimal('3.30')),
            (72, 'B', Decimal('3.00')),
            (67, 'B-', Decimal('2.70')),
            (62, 'C+', Decimal('2.50')),
            (57, 'C', Decimal('2.30')),
            (52, 'C-', Decimal('2.00')),
            (47, 'D+', Decimal('1.70')),
            (42, 'D', Decimal('1.50')),
            (35, 'F', Decimal('0.00')),
        ]
        
        for marks, expected_grade, expected_points in test_cases:
            result = ExamResult.objects.create(
                student=self.student,
                exam=self.exam,
                marks_obtained=Decimal(str(marks)),
                entered_by=self.faculty_user
            )
            
            self.assertEqual(result.grade, expected_grade)
            self.assertEqual(result.grade_points, expected_points)

class GradeModelTest(TestCase):
    def test_grade_creation(self):
        grade = Grade.objects.create(
            grade='A+',
            description='Outstanding',
            min_percentage=Decimal('90.00'),
            max_percentage=Decimal('100.00'),
            grade_points=Decimal('4.00'),
            is_pass=True
        )
        
        self.assertEqual(grade.grade, 'A+')
        self.assertEqual(grade.description, 'Outstanding')
        self.assertEqual(grade.grade_points, Decimal('4.00'))
        self.assertTrue(grade.is_pass)
        self.assertEqual(str(grade), 'A+ (Outstanding)')

class TranscriptModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.faculty_user = User.objects.create_user(
            username='testfaculty',
            email='faculty@test.com',
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

    def test_transcript_creation(self):
        transcript = Transcript.objects.create(
            student=self.student,
            semester=self.semester,
            total_credits=18,
            earned_credits=16,
            gpa=Decimal('3.50'),
            cgpa=Decimal('3.50'),
            academic_status='good_standing',
            generated_by=self.faculty_user
        )
        
        self.assertEqual(transcript.student, self.student)
        self.assertEqual(transcript.semester, self.semester)
        self.assertEqual(transcript.total_credits, 18)
        self.assertEqual(transcript.earned_credits, 16)
        self.assertEqual(transcript.gpa, Decimal('3.50'))
        self.assertEqual(transcript.cgpa, Decimal('3.50'))
        self.assertEqual(transcript.academic_status, 'good_standing')
        self.assertEqual(str(transcript), f"Transcript - {self.student} - {self.semester}")

class ExamAttendanceModelTest(TestCase):
    def setUp(self):
        # Create test data
        from courses.models import Course, Program, Semester
        from students.models import Student
        
        self.user = User.objects.create_user(
            username='teststudent',
            email='student@test.com',
            password='testpass123'
        )
        
        self.faculty_user = User.objects.create_user(
            username='testfaculty',
            email='faculty@test.com',
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
        
        self.course = Course.objects.create(
            course_code='CS101',
            course_name='Introduction to Programming',
            credits=3,
            program=self.program,
            semester=self.semester
        )
        
        self.student = Student.objects.create(
            user=self.user,
            roll_number='BSCS2024001',
            program=self.program,
            batch='BSCS-2024'
        )
        
        self.exam = Exam.objects.create(
            title='Mid Term Exam',
            exam_type='midterm',
            course=self.course,
            semester=self.semester,
            total_marks=100,
            pass_marks=40,
            duration_minutes=120,
            exam_date=date(2024, 12, 15),
            start_time=time(9, 0),
            end_time=time(11, 0),
            created_by=self.faculty_user
        )

    def test_exam_attendance_creation(self):
        check_in = datetime(2024, 12, 15, 8, 45, 0)
        check_out = datetime(2024, 12, 15, 11, 15, 0)
        
        attendance = ExamAttendance.objects.create(
            student=self.student,
            exam=self.exam,
            check_in_time=check_in,
            check_out_time=check_out,
            is_late=False,
            late_minutes=0,
            supervisor_remarks='Good behavior',
            recorded_by=self.faculty_user
        )
        
        self.assertEqual(attendance.student, self.student)
        self.assertEqual(attendance.exam, self.exam)
        self.assertEqual(attendance.check_in_time, check_in)
        self.assertEqual(attendance.check_out_time, check_out)
        self.assertFalse(attendance.is_late)
        self.assertEqual(attendance.late_minutes, 0)
        self.assertEqual(str(attendance), f"{self.student} - {self.exam} Attendance")

    def test_late_attendance(self):
        check_in = datetime(2024, 12, 15, 9, 15, 0)  # 15 minutes late
        
        attendance = ExamAttendance.objects.create(
            student=self.student,
            exam=self.exam,
            check_in_time=check_in,
            is_late=True,
            late_minutes=15,
            recorded_by=self.faculty_user
        )
        
        self.assertTrue(attendance.is_late)
        self.assertEqual(attendance.late_minutes, 15)
