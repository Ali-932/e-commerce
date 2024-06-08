from django.contrib import messages
from django.db import transaction
from django.db.models import Max, Sum, Count

from ecommerce.order.models import Order, OrderItem
from ecommerce.product.models import Volume


@transaction.atomic
def process_form(request, form, pk=None ,form_temp=None ,alternative_temp=None):
    if not request.user.is_authenticated:
        messages.error(request, 'يجب تسجيل الدخول اولا')
        return None, None
    cleaned_data = form.cleaned_data
    template = form_temp

    if request.POST.get('pk'):
        pk = request.POST.get('pk')
        template = alternative_temp

    order = Order.objects.filter(user=request.user, active=True).first()

    if not order:
        order = Order.objects.create(user=request.user, active=True)
    volume = Volume.objects.filter(pk=pk).select_related('product').first()

    order_item, created = OrderItem.objects.get_or_create(
        volume_id=pk,
        language=cleaned_data['language'],
        price=volume.price,
        order=order
    )

    order_item.quantity = cleaned_data['quantity']
    # orders= OrderItem.objects.select_related('volume','order').filter(order__user=request.user, order__active=True)
    # items_total_info=orders.aggregate(sum=Sum('price'),count=Count('id'))
    if created:
        messages.success(request, 'تم اضافه الطلب بنجاح')
    else:
        messages.info(request, 'تم تغيير الكمية')

    order_item.save()
    return volume, template
