from django.db import transaction
from django.db import transaction
from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.order.forms.order_form import OrderForm
from ecommerce.order.models import ShippingAddress
from ecommerce.order.utils.checkout_utils import order_save_and_modify_address
from ecommerce.settings import MEDIUM_REQUESTS_RATE_LIMIT, HEAVY_REQUESTS_RATE_LIMIT
from django.contrib import messages


@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
def checkout_page(request):
    if not request.user.is_authenticated:
        return permission_check(request)
    common = common_views(request)
    if common['total_count'] == 0:
        messages.error(request, 'لا توجد منتجات في السلة')
        return redirect('home:index')

    template = 'abstract/cart/checkout.html'
    try:
        initial_address = ShippingAddress.objects.get(user=request.user, is_active=True)
        initial_data = initial_address.__dict__
    except ShippingAddress.DoesNotExist:
        initial_address = None
        initial_data = {}
    form = OrderForm(request.POST or None, initial={**initial_data, 'is_active': False})

    if request.method == 'POST':
        template = 'abstract/order/orders.html'
        if form.is_valid():
            with transaction.atomic():
                return order_save_and_modify_address(
                    form, request, initial_address, template
                )
        elif not form.is_valid():
            template = 'abstract/cart/checkout.html'
            return render(request, template, {'form': form, **common})

    context = {
        'form': form,
        **common
    }
    return render(request, template, context)
