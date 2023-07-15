import re
from django import template

register = template.Library()


def replace(match):
    paragraph = match.group(0)
    tag = r'<p>'
    modified_tag = r'<p style="color: red;">'

    if replace.counter % 2 == 1:
        paragraph = re.sub(tag, modified_tag, paragraph)
    replace.counter += 1

    return paragraph


@register.filter
def alternate_paragraphs(value):
    replace.counter = 0
    pattern = r'<p>.*?</p>'

    return re.sub(pattern, replace, value)
