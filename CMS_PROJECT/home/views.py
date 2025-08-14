from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home_view(request):
    """
    
    """
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'faculty':
            return redirect('faculty_dashboard')
        elif request.user.role == 'student':
            return redirect('student_dashboard')
    else:
        # If not logged in, show Welcome page
        return render(request, 'home.html')
