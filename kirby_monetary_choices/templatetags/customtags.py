from django import template
from datetime import date, timedelta

register = template.Library()

@register.inclusion_tag('kirby_monetary_choices/tags/ContinueButton.html')
def continue_button(*args, **kwargs):
    return {}
