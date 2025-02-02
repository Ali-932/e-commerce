from django import template
import re

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import mark_safe

from ecommerce.home.models import Global

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


@register.filter
def arabic_intcomma(value):
    """
    Applies intcomma and replaces standard commas with Arabic commas.
    """
    value_with_commas = intcomma(value, use_l10n=False)
    return value_with_commas.replace(",", "،")


@register.simple_tag
def render_discounted_price(price):
    """
    Renders the original and discounted prices.

    If there is no discount (discount == 0), the original price is returned.
    Otherwise, the original price is shown with a strikethrough and the discounted price is highlighted.
    """
    discount = Global.get_instance().discount
    # No discount, return the original price formatted
    if discount == 0:
        price = arabic_intcomma(price)
        return mark_safe(f'<span class="price">{price} IQD</span>')

    # Calculate the discounted price
    discounted = price * (1 - discount / 100)
    price = arabic_intcomma(price)
    discounted = arabic_intcomma(discounted)
    # Build the HTML string with a non-breaking space between spans
    html = (
        f'<span class="original-price" style="text-decoration: line-through; color: red;">'
        f'IQD {price}'
        '</span>&nbsp;&nbsp;'
        f'<span class="discounted-price" style="color: green; font-weight: bold;">'
        f'IQD {discounted}'
        '</span>'
    )

    return mark_safe(html)