from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect
from djmoney.money import Money

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.home.models import Global
from ecommerce.order.forms.order_form import OrderForm
from ecommerce.order.models import Order, ShippingAddress


def checkout_page(request):
    if not request.user.is_authenticated:
        return permission_check(request)
    template = 'abstract/cart/checkout.html'
    try:
        initial_address = ShippingAddress.objects.get(user=request.user, is_active=True)
        initial_data= initial_address.__dict__
    except ShippingAddress.DoesNotExist:
        initial_address = None
        initial_data = {}
    form = OrderForm(request.POST or None, initial={**initial_data, 'is_active':False })

    if request.method == 'POST':
        template = 'abstract/cart/checkout.html'
        if form.is_valid():
            with transaction.atomic():
                cleaned_data = form.cleaned_data
                try:
                    order=Order.objects.get(user=request.user, active=True)
                except Order.DoesNotExist:
                    messages.error(request, 'لا يوجد طلبات لإتمام عملية الدفع')
                    return None,None
                order.status = Order.Status_CHOICES.CONFIRMED
                order.active = False
                order.total_price = Money(order.items.aggregate(total_price=Sum('price'))['total_price'],'IQD') + Global.get_instance().delivery_price
                order.save()
                if form.has_changed():
                    Address = form.save(commit=False)
                    if cleaned_data['defualt_address']:
                        Address.is_active = True
                        if initial_address:
                            initial_address.is_active = False
                            initial_address.save()
                    Address.order = order
                    Address.user = request.user
                    Address.save()
                common = common_views(request)
                return render(request, template, {'form': form, **common})
        elif not form.is_valid():
            return render(request, template, {'form': form})
    common = common_views(request)

    context = {
        'form': form,
        **common
    }
    return render(request, template, context)