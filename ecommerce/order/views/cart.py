from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.order.forms.order_form import OrderForm


def cart_page(request):
    template = 'abstract/cart/cart.html'
    menu_num, orders, total_info, nav_bar, authors = common_views(request)
    context = {
        'nav_ad': nav_bar,
        'menu_num': menu_num,
        'orders':orders,
        'total_price':total_info['sum'],
        'total_count':total_info['count'],
        'authors': authors
    }
    return render(request, template, context)