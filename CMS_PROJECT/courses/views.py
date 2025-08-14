from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Program, Semester, Course
from .forms import ProgramForm, SemesterForm, CourseForm

@login_required
def list_programs(request):
    programs = Program.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

@login_required
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_programs')
    else:
        form = ProgramForm()
    return render(request, 'add_program.html', {'form': form})

@login_required
def list_courses(request):
    courses = Course.objects.select_related('semester__program').all()
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_courses')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})
