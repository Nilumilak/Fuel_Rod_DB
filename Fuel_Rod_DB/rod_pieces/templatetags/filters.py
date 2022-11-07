import re
from django import template


register = template.Library()


def original_rod(value):
    pattern = re.compile(r'(.+)-R\d+')
    return pattern.findall(value)[0]


register.filter('original_rod', original_rod)
