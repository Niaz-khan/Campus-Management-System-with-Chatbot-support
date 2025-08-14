from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdmissionApplicationForm
from .models import AdmissionApplication

@login_required
def apply_for_admission(request):
    student = request.user.student_profile

    # Check if student already applied
    if hasattr(student, 'admission_application'):
        return render(request, 'already_applied.html')

    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.save()
            return redirect('student_dashboard')  # Redirect back to dashboard
    else:
        form = AdmissionApplicationForm()

    return render(request, 'apply.html', {'form': form})

@login_required
def view_applications(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')
    
    applications = AdmissionApplication.objects.select_related('student', 'program').all()
    return render(request, 'view_applications.html', {'applications': applications})
