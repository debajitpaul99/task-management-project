from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN PROGRESS", "In progress"),
        ("COMPLETED", "Completed")
    )
    assigned_to = models.ManyToManyField(User, related_name="tasks")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, blank=True, null=True, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

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
    asset = models.ImageField(upload_to="task_asset", blank=True, null=True, default="task_asset/default_img.jpg")

    def __str__(self):
        return f"{self.task.title}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("COMPLETED", "Completed"),
        ("ON HOLD", "On Hold")
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="ON HOLD")

    def __str__(self):
        return f"{self.name}"