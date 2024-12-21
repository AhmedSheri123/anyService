from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()


@register.simple_tag
@stringfilter
def get_ws_type(ss):
    a = settings.WS_TYPE
    return a