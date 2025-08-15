from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exam, ExamResult
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count, Max, Min, Sum, Q
from django.utils import timezone
from datetime import date, datetime
from decimal import Decimal

from .models import Exam, ExamSchedule, ExamResult, Grade, Transcript, ExamAttendance
from .serializers import (
    ExamSerializer, ExamScheduleSerializer, ExamResultSerializer,
    GradeSerializer, TranscriptSerializer, ExamAttendanceSerializer,
    StudentExamSummarySerializer, ExamAnalyticsSerializer
)
def add_exam_result(request):
    """
    View to add an exam result.
    Only accessible to faculty and admin users.
    """
    if request.user.role not in ['faculty', 'admin']:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        if form.is_valid():
            result = form.save()

            # ✅ After saving result, if it was a Final Exam, check promotion
            if result.exam.exam_type == 'final':
                promote_student_if_passed(result.student)

            return redirect('list_exam_results')
    else:
        form = ExamResultForm()
    return render(request, 'add_exam_result.html', {'form': form})

@login_required
def create_exam(request):
    """
    View to create a new exam.
    Only accessible to faculty and admin users.
    """
    # Check if the user is faculty or admin
    if request.user.role != 'faculty' and request.user.role != 'admin':
        return redirect('unauthorized')
    # check if the request method is POST
    # If it is, create a new exam form with the submitted data
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_exams')
    else:
        form = ExamForm()
    return render(request, 'create_exam.html', {'form': form})

@login_required
def list_exams(request):
    """
    View to list all exams.
    Only accessible to faculty and admin users.
    """
    exams = Exam.objects.select_related('course').all()
    return render(request, 'list_exams.html', {'exams': exams})


@login_required
def list_exam_results(request):
    """
    View to list all exam results.
    Only accessible to faculty and admin users.
    """
    results = ExamResult.objects.select_related('exam', 'student').all()
    return render(request, 'list_exam_results.html', {'results': results})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ExamResult
from .utils import calculate_grade, calculate_gpa

@login_required
def my_transcript(request):
    """
    View to display the student's transcript.
    Only accessible to students.
    """
    if request.user.role != 'student':
        return redirect('unauthorized')

    student = request.user.student

    results = ExamResult.objects.select_related('exam__course').filter(student=student)

    semesters = {}
    for result in results:
        semester_num = result.exam.course.semester.semester_number
        if semester_num not in semesters:
            semesters[semester_num] = []
        semesters[semester_num].append(result)

    # GPA per semester
    semester_gpas = {}
    for semester_num, exam_results in semesters.items():
        semester_gpas[semester_num] = calculate_gpa(exam_results)

    # Overall CGPA
    all_exam_results = list(results)
    overall_cgpa = calculate_gpa(all_exam_results)

    context = {
        'semesters': semesters,
        'semester_gpas': semester_gpas,
        'overall_cgpa': overall_cgpa,
    }

    return render(request, 'my_transcript.html', context)

class ExamViewSet(viewsets.ModelViewSet):
    """API endpoint for exam management"""
    queryset = Exam.objects.select_related(
        'course', 'semester', 'created_by'
    ).all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'title', 'course__course_code', 'course__course_name', 
        'exam_type', 'venue'
    ]
    ordering_fields = ['exam_date', 'start_time', 'created_at']

    @action(detail=False, methods=['get'])
    def upcoming_exams(self, request):
        """Get all upcoming exams"""
        today = date.today()
        upcoming = self.queryset.filter(
            exam_date__gte=today,
            status__in=['published', 'ongoing']
        ).order_by('exam_date', 'start_time')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def course_exams(self, request):
        """Get exams for a specific course"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': 'course_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        course_exams = self.queryset.filter(course_id=course_id)
        serializer = self.get_serializer(course_exams, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def semester_exams(self, request):
        """Get exams for a specific semester"""
        semester_id = request.query_params.get('semester_id')
        if not semester_id:
            return Response(
                {'error': 'semester_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        semester_exams = self.queryset.filter(semester_id=semester_id)
        serializer = self.get_serializer(semester_exams, many=True)
        return Response(serializer.data)

class ExamScheduleViewSet(viewsets.ModelViewSet):
    """API endpoint for exam schedule management"""
    queryset = ExamSchedule.objects.select_related(
        'student__user', 'exam__course', 'exam__semester'
    ).all()
    serializer_class = ExamScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'exam__title'
    ]
    ordering_fields = ['exam__exam_date', 'created_at']

    @action(detail=False, methods=['get'])
    def student_schedule(self, request):
        """Get exam schedule for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student_schedule = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(student_schedule, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exam_attendance(self, request):
        """Get attendance for a specific exam"""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response(
                {'error': 'exam_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exam_attendance = self.queryset.filter(exam_id=exam_id)
        serializer = self.get_serializer(exam_attendance, many=True)
        return Response(serializer.data)

class ExamResultViewSet(viewsets.ModelViewSet):
    """API endpoint for exam result management"""
    queryset = ExamResult.objects.select_related(
        'student__user', 'exam__course', 'entered_by'
    ).all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'exam__title'
    ]
    ordering_fields = ['marks_obtained', 'percentage', 'entered_at']

    @action(detail=False, methods=['get'])
    def student_results(self, request):
        """Get exam results for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student_results = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(student_results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exam_results(self, request):
        """Get results for a specific exam"""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response(
                {'error': 'exam_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exam_results = self.queryset.filter(exam_id=exam_id)
        serializer = self.get_serializer(exam_results, many=True)
        return Response(serializer.data)

class GradeViewSet(viewsets.ModelViewSet):
    """API endpoint for grade management"""
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['grade', 'description']
    ordering_fields = ['grade_points', 'min_percentage']

class TranscriptViewSet(viewsets.ModelViewSet):
    """API endpoint for transcript management"""
    queryset = Transcript.objects.select_related(
        'student__user', 'semester', 'generated_by'
    ).all()
    serializer_class = TranscriptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number'
    ]
    ordering_fields = ['gpa', 'cgpa', 'generated_at']

    @action(detail=False, methods=['get'])
    def student_transcript(self, request):
        """Get transcript for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        student_transcript = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(student_transcript, many=True)
        return Response(serializer.data)

class ExamAttendanceViewSet(viewsets.ModelViewSet):
    """API endpoint for exam attendance management"""
    queryset = ExamAttendance.objects.select_related(
        'student__user', 'exam', 'recorded_by'
    ).all()
    serializer_class = ExamAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'student__user__first_name', 'student__user__last_name',
        'student__roll_number', 'exam__title'
    ]
    ordering_fields = ['check_in_time', 'recorded_at']

class ExamAnalyticsViewSet(viewsets.ViewSet):
    """API endpoint for exam analytics and reporting"""
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def student_summary(self, request):
        """Get comprehensive exam summary for a student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get student's exam results
        results = ExamResult.objects.filter(student_id=student_id)
        total_exams = results.count()
        
        if total_exams == 0:
            return Response({
                'student_id': student_id,
                'message': 'No exam results found for this student'
            })

        # Calculate statistics
        total_marks = results.aggregate(total=Sum('marks_obtained'))['total'] or 0
        average_percentage = results.aggregate(avg=Avg('percentage'))['avg'] or 0
        
        # Get attendance data
        schedules = ExamSchedule.objects.filter(student_id=student_id)
        exams_attended = schedules.filter(attendance_status='present').count()
        exams_absent = schedules.filter(attendance_status='absent').count()
        
        # Get latest transcript for GPA
        latest_transcript = Transcript.objects.filter(student_id=student_id).order_by('-generated_at').first()
        gpa = latest_transcript.gpa if latest_transcript else 0
        academic_status = latest_transcript.get_academic_status_display() if latest_transcript else 'Not Available'

        summary_data = {
            'student_id': student_id,
            'student_name': results.first().student.user.get_full_name(),
            'semester': results.first().exam.semester.__str__(),
            'total_exams': total_exams,
            'exams_attended': exams_attended,
            'exams_absent': exams_absent,
            'total_marks': total_marks,
            'average_percentage': average_percentage,
            'gpa': gpa,
            'academic_status': academic_status,
        }

        serializer = StudentExamSummarySerializer(summary_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exam_analytics(self, request):
        """Get analytics for a specific exam"""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response(
                {'error': 'exam_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get exam details
        exam = Exam.objects.get(id=exam_id)
        
        # Get attendance data
        schedules = ExamSchedule.objects.filter(exam_id=exam_id)
        total_students = schedules.count()
        present_students = schedules.filter(attendance_status='present').count()
        absent_students = schedules.filter(attendance_status='absent').count()
        late_students = schedules.filter(attendance_status='late').count()
        
        # Get result data
        results = ExamResult.objects.filter(exam_id=exam_id)
        if results.exists():
            average_marks = results.aggregate(avg=Avg('marks_obtained'))['avg'] or 0
            highest_marks = results.aggregate(max=Max('marks_obtained'))['max'] or 0
            lowest_marks = results.aggregate(min=Min('marks_obtained'))['min'] or 0
            
            # Calculate pass rate
            pass_count = results.filter(marks_obtained__gte=exam.pass_marks).count()
            pass_rate = (pass_count / results.count()) * 100 if results.count() > 0 else 0
        else:
            average_marks = highest_marks = lowest_marks = pass_rate = 0

        analytics_data = {
            'exam_id': exam_id,
            'exam_title': exam.title,
            'total_students': total_students,
            'present_students': present_students,
            'absent_students': absent_students,
            'late_students': late_students,
            'average_marks': average_marks,
            'pass_rate': pass_rate,
            'highest_marks': highest_marks,
            'lowest_marks': lowest_marks,
        }

        serializer = ExamAnalyticsSerializer(analytics_data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def department_performance(self, request):
        """Get performance analytics for a department"""
        department_id = request.query_params.get('department_id')
        if not department_id:
            return Response(
                {'error': 'department_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all students in the department
        from students.models import Student
        students = Student.objects.filter(program__department_id=department_id)
        
        total_students = students.count()
        total_exams = 0
        total_marks = 0
        total_results = 0

        for student in students:
            results = ExamResult.objects.filter(student=student)
            total_results += results.count()
            total_marks += results.aggregate(total=Sum('marks_obtained'))['total'] or 0

        average_marks = total_marks / total_results if total_results > 0 else 0

        return Response({
            'department_id': department_id,
            'total_students': total_students,
            'total_exams_taken': total_results,
            'average_marks': average_marks,
        })
