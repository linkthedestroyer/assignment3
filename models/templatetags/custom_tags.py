from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines

register = template.Library()


def displayEnum(value: str):
    return value.replace("_", " ").capitalize()


def sanitize_for_js(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace("\n", " ").replace("\"", "\\\""))


sanitize_for_js.is_safe = True
remove_newlines = stringfilter(sanitize_for_js)
register.filter(remove_newlines)

register.filter("displayEnum", displayEnum)
