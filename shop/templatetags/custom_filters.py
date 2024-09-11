from django import template

register = template.Library()

@register.filter
def length_is(value, arg):
    """Проверяет, является ли длина value равной arg."""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False
