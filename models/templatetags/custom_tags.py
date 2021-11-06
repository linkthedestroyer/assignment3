from django import template

register = template.Library()


def displayEnum(value: str):
    return value.replace('_', ' ').capitalize()


register.filter('displayEnum', displayEnum)
