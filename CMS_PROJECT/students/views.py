from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm

@login_required
def my_profile(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return render(request, 'students/no_profile.html')
    return render(request, 'profile.html', {'student': student})

@login_required
def list_students(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')
    students = Student.objects.select_related('user', 'program').all()
    return render(request, 'list.html', {'students': students})

@login_required
def add_student(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # For now, link to existing user manually or add dummy user
            # student.user = some_user_reference
            student.save()
            return redirect('list_students')
    else:
        form = StudentForm()
    return render(request, 'add.html', {'form': form})
