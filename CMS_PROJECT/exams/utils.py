from courses.models import Semester, Course
from enrollments.models import Enrollment
from students.models import Student

def promote_student_if_passed(student):
    """
    Promotes a student to the next semester if they have passed all courses in the current semester.
    If the student has failed any course, they are not promoted.
    If the student has completed all semesters, their status is updated to 'graduated'.
    """
    # Step 1: Find student's current semester
    current_semester_numbers = student.enrollments.values_list('course__semester__semester_number', flat=True)
    if not current_semester_numbers:
        return False  # Student has no enrollments, cannot promote

    current_semester_number = max(current_semester_numbers)

    # Step 2: Check if failed any course in current semester
    failed_courses = student.exam_results.filter(
        marks_obtained__lt=50,
        exam__exam_type='final',
        exam__course__semester__semester_number=current_semester_number
    )

    if failed_courses.exists():
        return False  # Student failed at least one course — not promoted

    # Step 3: Promote to next semester
    next_semester = Semester.objects.filter(
        program=student.program,
        semester_number=current_semester_number + 1
    ).first()

    if next_semester:
        # Enroll in all next semester courses
        next_courses = Course.objects.filter(semester=next_semester)
        for course in next_courses:
            Enrollment.objects.create(student=student, course=course)
    else:
        # No next semester means student graduated
        student.status = 'graduated'
        student.save()

    return True  # Successfully promoted




def calculate_grade(marks):
    """
    Calculate the grade and GPA points based on marks obtained.
    """
    if marks < 0 or marks > 100:
        raise ValueError("Marks must be between 0 and 100.")
    else:
        if marks >= 85:
            return 'A', 4.0
        elif marks >= 75:
            return 'B+', 3.5
        elif marks >= 65:
            return 'B', 3.0
        elif marks >= 55:
            return 'C+', 2.5
        elif marks >= 50:
            return 'C', 2.0
        else:
            return 'F', 0.0

def calculate_gpa(exam_results):
    """
    Calculate the GPA based on exam results.
    """
    total_points = 0
    total_credits = 0

    for result in exam_results:
        grade, points = calculate_grade(result.marks_obtained)
        credits = result.exam.course.credits
        total_points += points * credits
        total_credits += credits

    if total_credits == 0:
        return 0.0

    gpa = total_points / total_credits
    return round(gpa, 2)
