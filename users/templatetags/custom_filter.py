from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def custom_time_format(value):
    if value:
        today = datetime.now().date()
        value = timezone.localdate(value)
        if value == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        if value == today.replace(day=today.day-1):
            return f"Yesterday at {value.strftime('%I:%M %p')}"