from django import template
from datetime import date, timedelta

register = template.Library()

@register.inclusion_tag('risk_from_experience_task/tags/ContinueButton.html')
def continue_button(*args, **kwargs):
    return {}
