from enrollments.models import Enrollment
from courses.models import Semester, Course

def auto_enroll_first_semester(student):
    """
    Automatically enroll a student in all courses for their first semester.
    This function is called when a new student is created.
    It finds the first semester for the student's program and enrolls them in all courses for that semester.
    """
    # Find Semester 1 for this student's program
    semester = Semester.objects.filter(program=student.program, semester_number=1).first()
    
    if semester:
        courses = Course.objects.filter(semester=semester)
        for course in courses:
            Enrollment.objects.create(student=student, course=course)
            print(f"Enrolled {student} in {course} for semester {semester.semester_number}.")
    else:   
        print(f"No Semester 1 found for program {student.program}.")