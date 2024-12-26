from django.contrib import messages
from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.settings import LIGHT_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='GET', rate=LIGHT_REQUESTS_RATE_LIMIT, block=True)
def cart_page(request):
    if not request.user.is_authenticated:
        return permission_check(request)
    common = common_views(request)
    if common['total_count'] == 0:
        messages.error(request, 'لا توجد منتجات في السلة')
        return redirect('home:index')


    template = 'abstract/cart/cart.html'
    context = {
        **common,
    }
    return render(request, template, context)