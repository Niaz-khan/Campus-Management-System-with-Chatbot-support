from django import template
from exams.utils import calculate_grade

register = template.Library()

@register.filter
def calculate_grade_display(marks):
    """
    Custom template filter to calculate the grade based on marks.
    """
    grade, _ = calculate_grade(marks)
    return grade
