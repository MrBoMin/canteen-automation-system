# your_app/templatetags/custom_filters.py
from django import template
from django.template.defaultfilters import slugify

register = template.Library()

@register.filter
def slugify(value):
    return slugify(value)
