from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)


'''
    how to use:
    {% load helpers %}
    {% with instance|content_type as ctype %}
        <input type="hidden" name="content_type" value="{{ ctype.pk }}">
    {% endwith %}
'''
