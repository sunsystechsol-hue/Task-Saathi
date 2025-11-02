from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import Task

@shared_task
def send_task_reminder_emails():
    """
    Send reminder emails for tasks due in the next 24 hours
    """
    tomorrow = datetime.now().date() + timedelta(days=1)
    tasks_due_soon = Task.objects.filter(dueDate=tomorrow, status='pending')
    
    for task in tasks_due_soon:
        if task.assignedTo.email:
            send_mail(
                subject=f'Reminder: Task "{task.title}" is due tomorrow',
                message=f'Your task "{task.title}" is due tomorrow. Please complete it on time.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[task.assignedTo.email],
                fail_silently=False,
            )
    
    return f"Sent {tasks_due_soon.count()} task reminder emails"

@shared_task
def clean_completed_tasks(days=30):
    """
    Archive tasks that have been completed for more than the specified days
    """
    cutoff_date = datetime.now().date() - timedelta(days=days)
    old_completed_tasks = Task.objects.filter(
        status='completed',
        updated_at__date__lte=cutoff_date
    )
    
    count = old_completed_tasks.count()
    # In a real implementation, you might move these to an archive table
    # For now, we'll just log the count
    
    return f"Processed {count} old completed tasks"