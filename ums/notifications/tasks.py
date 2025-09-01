from datetime import date, timedelta
from exams.models import Exam
from notifications.utils import send_notification

def notify_grading_deadline():
    today = date.today()
    reminder_date = today + timedelta(days=3)  # 3 days before deadline

    exams = Exam.objects.filter(
        result_status='DRAFT',
        date__lte=today
    )
    for exam in exams:
        if exam.grading_deadline() == reminder_date:
            send_notification(
                user=exam.created_by,
                title="Grading Deadline Reminder",
                message=f"Deadline for grading '{exam.title}' is approaching ({exam.grading_deadline()}).",
                related_object=exam
            )
