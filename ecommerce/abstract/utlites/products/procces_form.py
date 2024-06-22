from django.contrib import messages
from django.db import transaction

from ecommerce.order.models import Order, OrderItem
from ecommerce.product.models import Volume, SpecialOfferProducts


def _validate_quantity(cleaned_data, volume, view_page):
    form_quantity = cleaned_data['quantity']
    if view_page == 'special-offer':
        special_offer_product = SpecialOfferProducts.objects.get(volume=volume, is_available=True,
                                                                 language=cleaned_data['language'])
        if int(form_quantity) > int(special_offer_product.quantity):
            raise ValueError('حدثت مشكله اثناء معالجة الطلب')
    return form_quantity

@transaction.atomic
def process_form(request, form, view_page, pk=None, form_temp=None, alternative_temp=None):
    if not request.user.is_authenticated:
        messages.error(request, 'يجب تسجيل الدخول اولا')
        return None, None

    cleaned_data = form.cleaned_data
    template = alternative_temp if request.POST.get('pk') else form_temp
    pk = request.POST.get('pk') or pk

    order = Order.objects.filter(user=request.user, active=True).first()
    if not order:
        order = Order.objects.create(user=request.user, active=True)

    volume = Volume.objects.filter(pk=pk).select_related('product').first()
    if not volume:
        messages.error(request, 'المنتج غير موجود')
        return None, template

    try:
        price = _validate_price(cleaned_data, volume, view_page)
        quantity = _validate_quantity(cleaned_data, volume, view_page)
    except ValueError as e:
        messages.error(request, str(e))
        return None, template

    if cleaned_data['language'] not in ('AR', 'EN'):
        messages.error(request, 'حدثت مشكله اثناء معالجة الطلب')
        return None, template

    order_item, created = OrderItem.objects.get_or_create(
        volume_id=pk,
        language=cleaned_data['language'],
        price=price,
        order=order
    )
    order_item.quantity = quantity

    if created:
        messages.success(request, 'تم اضافه الطلب بنجاح')
    else:
        messages.info(request, 'تم تغيير الكمية')

    order_item.save()
    return volume, template


def _validate_price(cleaned_data, volume, view_page):
    form_price = cleaned_data['price']

    if view_page == 'special-offer':
        special_offer_product = SpecialOfferProducts.objects.get(volume=volume, is_available=True,
                                                                 language=cleaned_data['language'])
        database_price = special_offer_product.price.amount
    else:
        database_price = volume.price.amount

    if form_price != database_price:
        raise ValueError('حدثت مشكله اثناء معالجة الطلب')

    return form_price
