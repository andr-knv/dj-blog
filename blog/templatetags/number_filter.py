from django import template
from num2words import num2words

register = template.Library()


@register.filter
def num_to_text(val):
    words = val.split()
    modified_text = [num2words(int(w), lang='ru') if w.isdigit() else w for w in words]
    return ' '.join(modified_text)
