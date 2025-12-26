from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In progress"),
        ("COMPLETED", "Completed")
    )
    assigned_to = models.ManyToManyField(Employee)
    project = models.ForeignKey("Project",on_delete=models.CASCADE,default = 1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskDetails(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low")
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    priority = models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"Details for {self.task.title}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_after_creating_task(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        send_mail(
        "Task Assigned",
        f"You have been assigned to the task : {instance.title}",
        "debajit2003@gmail.com",
        assigned_emails, fail_silently=False)
