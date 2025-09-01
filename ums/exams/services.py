from .models import Grade
from .utils import percentage_to_grade_point

def calculate_student_cgpa(student):
    """
    Calculates and returns the CGPA and total credits for a given student.
    """
    grades = Grade.objects.filter(enrollment__student=student)
    total_points = 0
    total_credits = 0

    for grade in grades:
        percentage = (grade.marks_obtained / grade.exam.total_marks) * 100
        grade_points = percentage_to_grade_point(percentage)
        credit_hours = grade.enrollment.course.credit_hours
        total_points += grade_points * credit_hours
        total_credits += credit_hours

    cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0
    return cgpa, total_credits
