from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_after_creating_task(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        send_mail("Task Assigned",
        f"You have been assigned to the task : {instance.title}",
        "debajit2003@gmail.com",
        assigned_emails, fail_silently=False)