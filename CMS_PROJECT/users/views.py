from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'faculty':
                return redirect('faculty_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')
    return render(request, 'admin_dashboard.html')

@login_required
def faculty_dashboard(request):
    if request.user.role != 'faculty':
        return redirect('unauthorized')
    return render(request, 'faculty_dashboard.html')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('unauthorized')
    return render(request, 'student_dashboard.html')

def unauthorized_view(request):
    return render(request, 'unauthorized.html')
