from django.contrib import messages
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.settings import LIGHT_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='GET', rate=LIGHT_REQUESTS_RATE_LIMIT, block=True)
def cart_page(request):
    if not request.user.is_authenticated:
        return permission_check(request)

    template = 'abstract/cart/cart.html'
    common = common_views(request)
    context = {
        **common,
    }
    return render(request, template, context)