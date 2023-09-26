from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import render

from ecommerce.order.models import Order, OrderItem


def delete_order(request, pk: int):
    template='abstract/cart/cart.html'
    OrderItem.objects.get(pk=pk).delete()
    orders= OrderItem.objects.select_related('volume','order').filter(order__user=request.user)
    messages.error(request, 'تم ازالة المجلد من الطلبية')
    total_info=orders.aggregate(sum=Sum('volume__price'),count=Count('volume__id'))
    context = {
        'orders': orders,
        'total_price': total_info['sum'],
        'total_count': total_info['count']
    }

    return render(request,template,context)