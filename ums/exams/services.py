from .models import Grade

def percentage_to_grade_point(percentage: float) -> float:
    """
    Converts percentage to grade point based on a standard 4.0 scale.
    Adjust scale according to university policy if needed.
    """
    if percentage >= 85:
        return 4.0
    elif percentage >= 80:
        return 3.7
    elif percentage >= 75:
        return 3.3
    elif percentage >= 70:
        return 3.0
    elif percentage >= 65:
        return 2.7
    elif percentage >= 60:
        return 2.3
    elif percentage >= 55:
        return 2.0
    elif percentage >= 50:
        return 1.7
    else:
        return 0.0

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
