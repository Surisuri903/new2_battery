from django import template

register = template.Library()

@register.inclusion_tag('risk_from_description/tags/ContinueButton.html')
def continue_button(*args, **kwargs):
    return {}
