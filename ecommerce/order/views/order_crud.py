from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.order.models import OrderItem
from ecommerce.settings import HEAVY_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
def delete_order(request, pk: int):
    if not request.user.is_authenticated:
        return permission_check(request)
    template = 'abstract/cart/cart.html'
    OrderItem.objects.get(pk=pk).delete()
    items = OrderItem.objects.select_related('volume', 'order').filter(order__user=request.user, order__active=True)
    items_total_info = items.aggregate(sum=Sum('price'), count=Count('id'))
    messages.error(request, 'تم ازالة المجلد من الطلبية')
    common = common_views(request)

    context = {
        'items': items,
        'total_price': items_total_info['sum'],
        'total_count': items_total_info['count'],
        **common
    }

    return render(request, template, context)
