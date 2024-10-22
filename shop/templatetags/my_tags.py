from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def percentage_of(part, whole):
    try:
        return 100 * float(part) / float(whole)
    except (ValueError, ZeroDivisionError):
        return 0