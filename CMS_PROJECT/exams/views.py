from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Exam, ExamResult
from .forms import ExamForm, ExamResultForm
from .utils import promote_student_if_passed

@login_required
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
