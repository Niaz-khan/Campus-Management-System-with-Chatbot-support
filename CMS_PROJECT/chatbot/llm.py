from students.models import Student
from courses.models import Course, Semester
from enrollments.models import Enrollment
from exams.models import ExamResult
from transformers import pipeline
from langdetect import detect
import torch

# Load QA model
qa_pipeline = pipeline(
    "question-answering", 
    model="distilbert-base-cased-distilled-squad",
    device=0 if torch.cuda.is_available() else -1
)

# Load translation models (Urdu)
en_to_ur_translator = pipeline("translation_en_to_ur", 
    model="Helsinki-NLP/opus-mt-en-ur",
    device=0 if torch.cuda.is_available() else -1
)

ur_to_en_translator = pipeline("translation_ur_to_en", 
    model="Helsinki-NLP/opus-mt-ur-en",
    device=0 if torch.cuda.is_available() else -1

)

def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'en'

def detect_intent(question):
    # Simple intent detection based on keywords
    # This is a placeholder. You can replace it with a more sophisticated model if needed.
    q = question.lower().strip()

    greetings = ["hi", "hello", "salam", "hey", "assalamualaikum"]
    if any(greet in q for greet in greetings):
        return "greeting"
    elif "gpa" in q:
        return "gpa"
    elif "course" in q or "subject" in q:
        return "courses"
    elif "promoted" in q or "promotion" in q:
        return "promotion"
    elif "transcript" in q or "result" in q:
        return "transcript"
    else:
        return "general"

def ask_huggingface_model(question, context="Smart University Management System. Students are enrolled in courses and promoted semester by semester. GPA is calculated based on marks."):
    detected_lang = detect_language(question)
    english_question = question # Assume English by default

    if detected_lang == 'ur':
        english_question = ur_to_en_translator(question)[0]['translation_text']
        print(f"Translated Urdu to English: {english_question}")
    elif detected_lang == 'ps':
        return "Sorry, Pashto translation is not supported right now." # Fallback for Pashto

    response = qa_pipeline(question=english_question, context=context)
    english_answer = response['answer']
    print(f"English Answer: {english_answer}")

    if detected_lang == 'ur':
        final_answer = en_to_ur_translator(english_answer)[0]['translation_text']
        print(f"Translated English to Urdu: {final_answer}")
        return final_answer

    return english_answer # Return English answer for English or other languages

def handle_real_data(question, user=None):
    intent = detect_intent(question)

    if intent == "greeting":
        return "Hello! How can I assist you in your university matters?"
    elif intent == "gpa":
        return get_student_gpa(user)
    elif intent == "courses":
        return get_student_courses(user)
    elif intent == "promotion":
        return check_promotion_status(user)
    elif intent == "transcript":
        return generate_transcript_summary(user)
    else:
        return ask_huggingface_model(question)




def get_student_gpa(user):
    """
    Calculate the GPA of a student based on their exam results.
    """
    try:
        student = user.student
    except:
        return "Student profile not found."

    exam_results = ExamResult.objects.filter(student=student)
    if not exam_results.exists():
        return "No exam results found."

    total_points = 0
    total_credits = 0
    for result in exam_results:
        marks = result.marks_obtained
        credits = result.exam.course.credits
        if marks >= 85:
            points = 4.0
        elif marks >= 75:
            points = 3.5
        elif marks >= 65:
            points = 3.0
        elif marks >= 55:
            points = 2.5
        elif marks >= 50:
            points = 2.0
        else:
            points = 0.0

        total_points += points * credits
        total_credits += credits

    gpa = total_points / total_credits if total_credits else 0
    return f"Your current CGPA is {round(gpa, 2)}."

def get_student_courses(user):
    """
    Get the list of courses a student is enrolled in.
    """
    try:
        student = user.student
    except:
        return "Student profile not found."

    enrollments = Enrollment.objects.filter(student=student)
    if not enrollments.exists():
        return "You are not enrolled in any courses."

    course_names = [e.course.course_name for e in enrollments]
    return "Your enrolled courses are: " + ", ".join(course_names)

def check_promotion_status(user):
    """
    Check if a student is promoted to the next semester.
    """
    try:
        student = user.student
    except:
        return "Student profile not found."

    semesters = student.enrollments.values_list('course__semester__semester_number', flat=True)
    if not semesters:
        return "No semester information found."

    current_semester = max(semesters)
    total = Semester.objects.filter(program=student.program).count()

    if current_semester >= total:
        return "Congratulations! You have completed all semesters."
    else:
        return f"You are currently in Semester {current_semester}."

def generate_transcript_summary(user):
    """
    Generate a summary of the student's exam results for the transcript.
    1. Get the student object from the user.

    """

    try:
        student = user.student
    except:
        return "Student profile not found."

    results = ExamResult.objects.select_related('exam__course').filter(student=student)
    if not results.exists():
        return "No exam results to generate transcript."

    lines = []
    for result in results:
        course = result.exam.course
        lines.append(f"{course.course_code} - {course.course_name}: {result.marks_obtained} marks")

    return "Transcript Summary:\n" + "\n".join(lines)

