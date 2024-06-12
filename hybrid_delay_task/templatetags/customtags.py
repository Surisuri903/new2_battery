from django import template
from datetime import date, timedelta

register = template.Library()


@register.inclusion_tag('hybrid_delay_task/tags/ContinueButton.html')
def continue_button(*args, **kwargs):
    return {}
