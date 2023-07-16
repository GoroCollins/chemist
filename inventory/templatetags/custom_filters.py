from django.utils import timezone
from django import template
from datetime import datetime
register = template.Library()
@register.filter
def greeting(value):
    # Get the current time
    current_time = datetime.now().time()
    # Convert the time to hours
    current_hour = current_time.hour
    # Determine the time category
    if 5 <= current_hour < 12:
        time_category = "morning"
    elif 12 <= current_hour < 17:
        time_category = "afternoon"
    elif 17 <= current_hour < 20:
        time_category = "evening"
    else:
        time_category = "night"
    return f"Good {time_category}"