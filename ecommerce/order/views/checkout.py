from django.db import transaction
from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.order.forms.order_form import OrderForm
from ecommerce.order.models import Order, ShippingAddress


def checkout_page(request):
    template = 'abstract/cart/checkout.html'
    initial_address = ShippingAddress.objects.get(user=request.user, is_active=True)
    form = OrderForm(request.POST or None, initial={**initial_address.__dict__, 'is_active':False })

    if request.method == 'POST':
        if form.is_valid():
            with transaction.atomic():
                cleaned_data = form.cleaned_data
                order=Order.objects.get(user=request.user, active=True)
                order.status = Order.Status_CHOICES.CONFIRMED
                order.active = False
                order.save()
                if form.has_changed():
                    Address = form.save(commit=False)
                    if cleaned_data['defualt_address']:
                        Address.is_active = True
                        initial_address.is_active = False
                        initial_address.save()
                    Address.order = order
                    Address.user = request.user
                    Address.save()
                return render(request, template, {'form': form})
        elif not form.is_valid():
            return render(request, template, {'form': form})
    menu_num, orders, total_info, nav_bar, authors = common_views(request)

    context = {
        'nav_ad': nav_bar,
        'menu_num': menu_num,
        'orders':orders,
        'total_price':total_info['sum'],
        'total_count':total_info['count'],
        'authors': authors,
        'form': form
    }
    return render(request, template, context)