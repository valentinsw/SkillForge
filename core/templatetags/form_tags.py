# core/templatetags/form_tags.py
from django import template
from .forms import add_class as _add_class  # reuse the existing filter from core/templatetags/forms.py

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """Mirror of the 'add_class' filter exposed under 'form_tags' library."""
    return _add_class(field, css)

