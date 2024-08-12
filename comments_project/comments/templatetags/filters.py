from django import template

register = template.Library()


@register.filter
def with_avatars_prefix(value):
    return f'/media/avatars/{value}'
