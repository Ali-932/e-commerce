from django.contrib import messages
from django.db import transaction

from ecommerce.order.models import Order, OrderItem
from ecommerce.product.models import Volume, InventoryProduct, Item
from django.shortcuts import get_object_or_404


def _validate_quantity(cleaned_data, volume):
    form_quantity = cleaned_data['quantity']
    item = Item.objects.get(id=volume)
    if item.type == Item.Type_CHOICES.InventoryProduct:
        special_offer_product = InventoryProduct.objects.get(pk=volume, is_available=True,
                                                             language=cleaned_data['language'])
        if int(form_quantity) > int(special_offer_product.quantity):
            raise ValueError('حدثت مشكله اثناء معالجة الطلب')
    return form_quantity


@transaction.atomic
def process_form(request, form, pk=None, form_temp=None, alternative_temp=None):
    if not request.user.is_authenticated:
        messages.error(request, 'يجب تسجيل الدخول اولا')
        return None, None

    cleaned_data = form.cleaned_data
    template = alternative_temp if request.POST.get('pk') else form_temp
    pk = request.POST.get('pk') or pk

    order = Order.objects.filter(user=request.user, active=True).first()
    if not order:
        order = Order.objects.create(user=request.user, active=True)

    volume = Item.objects.filter(pk=pk).select_related('product').first()
    if not volume:
        messages.error(request, 'المنتج غير موجود')
        return None, template

    try:
        price = _validate_price(cleaned_data, pk)
        quantity = _validate_quantity(cleaned_data, pk)
    except ValueError as e:
        messages.error(request, str(e))
        return None, template

    if cleaned_data['language'] not in ('AR', 'EN'):
        messages.error(request, 'حدثت مشكله اثناء معالجة الطلب')
        return None, template
    order_item, created = OrderItem.objects.get_or_create(
        item_id=pk,
        language=cleaned_data['language'],
        order=order
    )
    order_item.quantity = quantity
    order_item.price = price
    if created:
        messages.success(request, 'تم اضافه الطلب بنجاح')
    else:
        messages.info(request, 'تم تغيير الكمية')

    order_item.save()
    return volume, template


def _validate_price(cleaned_data, pk):
    form_price = cleaned_data['price']
    item = get_object_or_404(Item, pk=pk)
    if item.type == Item.Type_CHOICES.InventoryProduct:
        item = InventoryProduct.objects.filter(pk=pk, is_available=True,
                                               language=cleaned_data['language']).first()
        if not item:
            raise ValueError('حدثت مشكله اثناء معالجة الطلب')
    database_price = item.price.amount

    if form_price != database_price:
        raise ValueError('حدثت مشكله اثناء معالجة الطلب')

    return form_price
