from django.contrib import messages
from django.db.models import Sum, OuterRef, Subquery
from django.shortcuts import render
from djmoney.money import Money

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.home.models import Global
from ecommerce.order.models import Order
import requests

from ecommerce.product.models import SpecialOfferProducts
from ecommerce.settings import SPREADSHEET_API


def remove_item_if_special_offer(items):
    # sop = SpecialOfferProducts.objects.filter(volume__in=items.values('volume_id'), is_available=True, language=languages)
    # Assuming items is a queryset
    items_subquery = items.filter(volume_id=OuterRef('volume_id')).values('language')[:1]

    sop = SpecialOfferProducts.objects.filter(
        volume__in=items.values('volume_id'),
        is_available=True,
        language=Subquery(items_subquery)
    )


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
    cleaned_data = form.cleaned_data
    try:
        order = Order.objects.get(user=request.user, active=True)
    except Order.DoesNotExist:
        messages.error(request, 'لا يوجد طلبات لإتمام عملية الدفع')
        return None, None
    order.status = Order.Status_CHOICES.CONFIRMED
    # when an order is active every order item is added to it
    order.active = False
    order.total_price = Money(order.items.aggregate(total_price=Sum('price'))['total_price'],
                              'IQD') + Global.get_instance().delivery_price
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
    common = common_views(request)
    items = order.items.all()
    send_order_to_sheet(cleaned_data, order, request.user, items)
    remove_item_if_special_offer(items)
    return render(request, template, {'form': form, **common})

def send_order_to_sheet(cleaned_data, order, user, items):
    order_str = ''
    languages = set()
    for item in items:
        order_str += f'{item.volume.product.name} vol {item.volume.volume_number} X {item.quantity} {item.language}) \n'
        languages.add(item.language)
    language = languages.pop() if len(languages) == 1 else 'MIXED'
    order_dict = {
        'data':{
        'USER': user.username,
        'INSTA': cleaned_data['instagram_username'],
        'ADDRESS': cleaned_data['province'] + cleaned_data['address'],
        'ORDER': order_str,
        'LANG': language,
        'Count': order.total_quantity,
        'Deliv': float(Global.get_instance().delivery_price.amount),
        'PRICE': float(order.total_price.amount),
        'PHONE': f'{cleaned_data["phone"]} \n {cleaned_data["phone2"] or ""}',
        'STATUS': order.status,
        'DATE': str(order.updated_at.date()),
        }}
    print(order_dict)
    post_to_sheet = requests.post(SPREADSHEET_API, json=order_dict)

    if post_to_sheet.status_code == 200:
        print('order sent to sheet')
    else:
        print('order not sent to sheet')
        print(post_to_sheet.json())