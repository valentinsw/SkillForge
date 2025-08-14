# core/templatetags/forms.py
from django import template

register = template.Library()

@register.filter
def add_class(field, css):
    """Append CSS classes to a field's widget."""
    existing = field.field.widget.attrs.get("class", "")
    attrs = {"class": (existing + " " + css).strip()}
    return field.as_widget(attrs=attrs)

# ---- Helpers so templates don't touch __class__ etc. ----

def _widget(obj):
    """Return a widget given a BoundField or a widget."""
    return getattr(getattr(obj, "field", None), "widget", obj)

@register.filter
def widget_type(obj):
    """Return the widget class name (e.g. 'TextInput', 'Select')."""
    return _widget(obj).__class__.__name__

@register.filter
def input_type(obj):
    """Return widget.input_type if present (e.g. 'text', 'checkbox', 'file')."""
    return getattr(_widget(obj), "input_type", "") or ""

@register.filter
def is_checkbox(obj):
    return input_type(obj) == "checkbox"

@register.filter
def is_file(obj):
    return input_type(obj) == "file"

@register.filter
def is_select(obj):
    return widget_type(obj) in ("Select", "SelectMultiple")

