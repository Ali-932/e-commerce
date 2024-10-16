from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='remove_brackets')
def remove_brackets(value:list):
    return ' | '.join(value)


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    '''
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' bar='two' baz=99 %} outputs ?foo=one&bar=two&baz=99

    A RequestContext is required for access to the current querystring.
    '''
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()

@register.simple_tag(name='score_filter')
def score_filter(value):
    value = float(value)
    if value >= 7:
        return mark_safe(f'<span style="color: green;">التقييم :{value}</span>')
    elif 5 <= value < 7:
        return mark_safe(f'<span style="color: #8B8000;">التقييم :{value}</span>')
    else:
        return mark_safe(f'<span style="color: red;">التقييم :{value}</span>')
