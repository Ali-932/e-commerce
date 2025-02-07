import json

from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, OuterRef, Subquery
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from djmoney.money import Money

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.home.models import Global
from ecommerce.order.models import Order
import requests

from ecommerce.product.models import InventoryProduct, Item
from ecommerce.settings import SPREADSHEET_API


def remove_item_if_special_offer(request, items):
    # sop = InventoryProduct.objects.filter(volume__in=items.values('volume_id'), is_available=True, language=languages)
    # Assuming items is a queryset

    for item in items:
        if item.item.type == Item.Type_CHOICES.InventoryProduct:
            sop = InventoryProduct.objects.filter(volume=item.item.volume.pk, is_available=True, language=item.language)
            if sop.exists():
                sop = sop.first()
                if sop.quantity <= 0:
                    messages.error(request, 'العنصر غير متوفر حالياً')
                    raise ValueError('العنصر غير متوفر حالياً')
                sop.quantity -= 1
                sop.save()
            else:
                item = items.get(pk=item.pk)
                item.delete()
                return False
    return True
    # items_subquery = items.filter(volume_id=OuterRef('volume_id')).values('language')[:1]
    #
    # sop = InventoryProduct.objects.filter(
    #     volume__in=items.values('volume_id'),
    #     is_available=True,
    #     language=Subquery(items_subquery)
    # )


def order_save_and_modify_address(form, request, initial_address, template):
    """
    Save the order, modify the address, and render the checkout template.

    Args:
        form: The form containing the address information.
        request: The HTTP request object.
        initial_address: The initial address object.
        template: The template to render.

    Returns:
        Tuple containing the rendered HTTP response and common context data.

    Raises:
        None

    """
    with transaction.atomic():
        cleaned_data = form.cleaned_data
        try:
            order = Order.objects.get(user=request.user, active=True)
        except Order.DoesNotExist:
            messages.error(request, 'لا يوجد طلبات لإتمام عملية الدفع')
            return None, None
        items = order.items.all()
        are_items_there = remove_item_if_special_offer(request, items)
        if not are_items_there:
            messages.error(request, 'العنصر الذي كان في السلة غير متوفر')
            return redirect('home:index')
        order.status = Order.Status_CHOICES.CONFIRMED
        # when an order is active every order item is added to it
        order.active = False
        order.total_price = Money(order.items.aggregate(total_price=Sum('price'))['total_price'],
                                  'IQD') + Global.get_instance().delivery_price
        order.total_quantity = order.items.aggregate(total_quantity=Sum('quantity'))['total_quantity']
        order.save()
        # if the address form is changed and default address is checked then the old address is deactivated
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
        messages.success(request, 'تم ارسال الطلب بنجاح')
        response = redirect('orders:view_orders')
        order_data = {
            'total_price': float(order.total_price.amount),
            'number_items': order.total_quantity
        }
        response.set_cookie('ordered', json.dumps(order_data), max_age=10)
        return response