from django.contrib import messages
from django.db.models import Sum, Count
from django.shortcuts import render, redirect

from ecommerce.abstract.utlites.permission_check import permission_check
from ecommerce.order.models import Order, OrderItem


def delete_order(request, pk: int):
    if not request.user.is_authenticated:
        return permission_check(request)
    template='abstract/cart/cart.html'
    OrderItem.objects.get(pk=pk).delete()
    items= OrderItem.objects.select_related('volume','order').filter(order__user=request.user,order__active=True)
    items_total_info=items.aggregate(sum=Sum('price'),count=Count('id'))
    messages.error(request, 'تم ازالة المجلد من الطلبية')
    context = {
        'items': items,
        'total_price': items_total_info['sum'],
        'total_count': items_total_info['count']
    }

    return render(request,template,context)