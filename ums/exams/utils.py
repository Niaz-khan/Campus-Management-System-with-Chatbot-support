
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
