import re

from django import template
from num2words import num2words

register = template.Library()


@register.filter
def num_to_text(val):
    pattern = r'\d+'

    return re.sub(
        pattern,
        lambda match: num2words(int(match.group(0)), lang='ru'),
        val
    )
