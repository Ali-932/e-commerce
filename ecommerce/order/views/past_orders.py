from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.settings import MEDIUM_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def view_orders(request):
    if not request.user.is_authenticated:
        return permission_check(request)

    template='abstract/order/orders.html'
    common = common_views(request)

    context = {
        **common,
    }

    return render(request,template,context)