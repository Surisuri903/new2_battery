from django import template
from datetime import date, timedelta

register = template.Library()

@register.inclusion_tag('tower_of_london/tags/ContinueButton.html')
def continue_button(*args, **kwargs):
    return {}
