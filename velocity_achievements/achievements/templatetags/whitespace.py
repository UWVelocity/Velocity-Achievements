from django import template
import re

register = template.Library()

single_newlines = (re.compile(r'(?<!\n)\n(?!\n)'), '',)
consecutive_newlines = (re.compile(r'\n\n'), '\n',)
strip_whitespace = (re.compile(r'(^ +)|( +$)', flags=re.M), '',)
repeated_whitespace = (re.compile(r'  +'), ' ',)

@register.filter
def tidy_whitespace(content):
    for transform in (single_newlines, consecutive_newlines,
            strip_whitespace, repeated_whitespace):
        content = re.sub(transform[0], transform[1], content)
    return content.strip()
