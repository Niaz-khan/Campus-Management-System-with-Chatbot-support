from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from .forms import EnrollmentForm
from admissions.models import AdmissionApplication
from .utils import auto_enroll_first_semester

@login_required
def enroll_student(request):
    """
    View to enroll a student in a course.
    Only accessible to students.
    """
    if request.user.role != 'student':
        return redirect('unauthorized')

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my_enrollments')
    else:
        form = EnrollmentForm()

    return render(request, 'enroll.html', {'form': form})

@login_required
def my_enrollments(request):
    """
    View to display the courses a student is enrolled in.
    Only accessible to students.
    """
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    return render(request, 'my_enrollments.html', {'enrollments': enrollments})


@login_required
def accept_application(request, application_id):
    """
    View to accept an admission application.
    Only accessible to admin users.
    """
    if request.user.role != 'admin':
        return redirect('unauthorized')

    application = AdmissionApplication.objects.get(id=application_id)
    application.status = 'accepted'
    application.save()

    # ✅ Auto-enroll student into 1st semester courses
    student = application.student
    auto_enroll_first_semester(student)

    return redirect('view_applications')
