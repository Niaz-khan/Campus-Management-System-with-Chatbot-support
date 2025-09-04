from decimal import Decimal
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone

def try_import(path):
    """Import a model by dotted path; return None if missing."""
    try:
        module_path, name = path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[name])
        return getattr(module, name)
    except Exception:
        return None

def admin_metrics(filters=None, date_from=None, date_to=None):
    filters = filters or {}
    today = timezone.now().date()

    # Default results
    res = dict(
        total_students=0,
        total_faculty=0,
        total_enrollments=0,
        fees_collected=Decimal('0.00'),
        fees_overdue=Decimal('0.00'),
        attendance_avg_percent=0.0,
        avg_gpa=0.0,
        hostel_occupancy_percent=0.0,
        cafeteria_active_subscriptions=0,
        transport_active_passes=0,
        sports_active_memberships=0,
    )

    # Users / Students / Faculty
    User = try_import('users.models.User')
    StudentProfile = try_import('students.models.StudentProfile')
    Enrollment = try_import('enrollments.models.Enrollment')
    Attendance = try_import('attendance.models.Attendance')
    Invoice = try_import('fees.models.Invoice')
    Grade = try_import('exams.models.Grade')
    HostelAllocation = try_import('hostel.models.Allocation') or try_import('hostel.models.HostelAllocation')
    HostelRoom = try_import('hostel.models.Room')
    MealSubscription = try_import('cafeteria.models.MealSubscription')
    TransportPass = try_import('transport.models.TransportPass')
    GymMembership = try_import('sports.models.GymMembership')

    # Filters (batch_id, program_id) scoping enrollments/attendance/grades/fees
    batch_id = filters.get('batch_id')
    program_id = filters.get('program_id')

    # Total students / faculty
    if User:
        res['total_faculty'] = User.objects.filter(role='FACULTY').count()
    if StudentProfile:
        qs = StudentProfile.objects.all()
        if batch_id: qs = qs.filter(batch_id=batch_id)
        if program_id: qs = qs.filter(program_id=program_id)
        res['total_students'] = qs.count()

    # Enrollments
    if Enrollment:
        qs = Enrollment.objects.all()
        if batch_id: qs = qs.filter(student__batch_id=batch_id)
        if program_id: qs = qs.filter(student__program_id=program_id)
        if date_from: qs = qs.filter(created_at__date__gte=date_from)
        if date_to: qs = qs.filter(created_at__date__lte=date_to)
        res['total_enrollments'] = qs.count()

    # Fees
    if Invoice:
        inv = Invoice.objects.all()
        if batch_id: inv = inv.filter(student__batch_id=batch_id)
        if program_id: inv = inv.filter(student__program_id=program_id)
        collected = inv.filter(is_paid=True).aggregate(s=Sum('amount'))['s'] or Decimal('0')
        overdue = inv.filter(is_paid=False, due_date__lt=today).aggregate(s=Sum('amount'))['s'] or Decimal('0')
        res['fees_collected'] = collected
        res['fees_overdue'] = overdue

    # Attendance average %
    if Attendance:
        att = Attendance.objects.all()
        if batch_id: att = att.filter(enrollment__student__batch_id=batch_id)
        if program_id: att = att.filter(enrollment__student__program_id=program_id)
        total = att.count()
        present = att.filter(status='PRESENT').count()
        res['attendance_avg_percent'] = (present / total * 100) if total else 0.0

    # Grades → avg GPA (assumes Grade has numeric gpa or grade_points)
    if Grade:
        # try grade_points or gpa field names
        avg = (Grade.objects
               .filter(**({'student__batch_id': batch_id} if batch_id else {}))
               .filter(**({'student__program_id': program_id} if program_id else {}))
               .aggregate(a=Avg('gpa'))['a'])
        if avg is None:
            avg = Grade.objects.aggregate(a=Avg('grade_points'))['a']
        res['avg_gpa'] = float(avg) if avg else 0.0

    # Hostel occupancy
    if HostelAllocation and HostelRoom:
        total_beds = HostelRoom.objects.aggregate(s=Sum('capacity'))['s'] or 0
        active_alloc = HostelAllocation.objects.filter(active=True).count()
        res['hostel_occupancy_percent'] = (active_alloc / total_beds * 100) if total_beds else 0.0

    # Cafeteria subscriptions
    if MealSubscription:
        res['cafeteria_active_subscriptions'] = MealSubscription.objects.filter(active=True).count()

    # Transport passes
    if TransportPass:
        res['transport_active_passes'] = TransportPass.objects.filter(is_active=True).count()

    # Sports memberships
    if GymMembership:
        res['sports_active_memberships'] = GymMembership.objects.filter(is_active=True).count()

    return res


def faculty_metrics(user, filters=None, date_from=None, date_to=None):
    """Scope data to faculty’s assigned courses/batches if available:
       Assumes FacultyProfile has relations; falls back to intersections via Enrollment.course__faculty=user."""
    filters = filters or {}
    res = dict(
        my_students=0,
        my_enrollments=0,
        my_attendance_avg_percent=0.0,
        my_avg_grade=0.0,
    )

    Enrollment = try_import('enrollments.models.Enrollment')
    Attendance = try_import('attendance.models.Attendance')
    Grade = try_import('exams.models.Grade')

    if Enrollment:
        my_enr = Enrollment.objects.filter(course__faculty=user)  # adjust if your model differs
        if date_from: my_enr = my_enr.filter(created_at__date__gte=date_from)
        if date_to: my_enr = my_enr.filter(created_at__date__lte=date_to)
        res['my_enrollments'] = my_enr.count()
        res['my_students'] = my_enr.values('student_id').distinct().count()

    if Attendance:
        my_att = Attendance.objects.filter(enrollment__course__faculty=user)
        total = my_att.count()
        present = my_att.filter(status='PRESENT').count()
        res['my_attendance_avg_percent'] = (present / total * 100) if total else 0.0

    if Grade:
        my_gr = Grade.objects.filter(course__faculty=user)
        avg = my_gr.aggregate(a=Avg('gpa'))['a']
        if avg is None:
            avg = my_gr.aggregate(a=Avg('grade_points'))['a']
        res['my_avg_grade'] = float(avg) if avg else 0.0

    return res
