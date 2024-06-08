from django.db import transaction
from django.db import transaction
from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.order.forms.order_form import OrderForm
from ecommerce.order.models import ShippingAddress
from ecommerce.order.utils.checkout_utils import order_save_and_modify_address


def checkout_page(request):
    if not request.user.is_authenticated:
        return permission_check(request)
    template = 'abstract/cart/checkout.html'
    try:
        initial_address = ShippingAddress.objects.get(user=request.user, is_active=True)
        initial_data = initial_address.__dict__
    except ShippingAddress.DoesNotExist:
        initial_address = None
        initial_data = {}
    form = OrderForm(request.POST or None, initial={**initial_data, 'is_active': False})

    if request.method == 'POST':
        template = 'abstract/cart/checkout.html'
        if form.is_valid():
            with transaction.atomic():

                return order_save_and_modify_address(
                    form, request, initial_address, template
                )
        elif not form.is_valid():
            return render(request, template, {'form': form})
    common = common_views(request)

    context = {
        'form': form,
        **common
    }
    return render(request, template, context)