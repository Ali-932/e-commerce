from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Max
from django.http import HttpRequest
from django.db.models import Count, F, Window
from django.db.models.functions import RowNumber

from ecommerce.home.models import nav_ad as NAV, Global
from ecommerce.abstract.utlites.menu_nums import menu_nums
# def _common_base_View(request: HttpRequest,
#                       model,
#                       query,
#                       # filters_callable: Callable,
#                       *,
#                       search_q: str,
#                       extra_callable,
#                       only_fields: list = None,
#                       ) -> dict:
#
#     per_page = int(request.GET.get('per_page', 10))
#     page = int(request.GET.get('page', 1))
#     q = request.GET.get('q', '')
#     is_nav = request.GET.get('nav', False)
#     if request.htmx and is_nav or not request.htmx:
#         if only_fields:
#             objs = query.only(*only_fields)
#         try:
#             nav_ad = NAV.objects.get(active=True)
#         except ObjectDoesNotExist:
#             nav_ad = None
#
#     return nav_ad
from ecommerce.order.models import OrderItem, Order
from ecommerce.product.models import Volume


def common_views(request):
    nav_bar = 0 if request.htmx else NAV.objects.get(active=True) # we only need the nav bar if we are refreshing the page
    authors = Volume.objects.filter(
        product__score__gt=8).values('product__author').annotate(max_score=Max('product__score')).order_by('-max_score')[:10]
    authors = [
        f"{list(item['product__author'].keys())[0]} - {list(item['product__author'].keys())[1]}"
        if len(list(item['product__author'].keys())) > 1
        else f"{list(item['product__author'].keys())[0]}"
        for item in authors
    ]
    if request.user.is_authenticated:
        items = OrderItem.objects.select_related('volume', 'order').filter(order__user=request.user, order__active=True)
        items_total_info = items.aggregate(sum=Sum('price'), count=Count('id'))
        orders = Order.objects.filter(user=request.user, active=False).annotate(serial=Window(
            expression=RowNumber(),
            order_by=F('id').asc()
        ))
        order_total_info = orders.aggregate(count=Count('id'))
    else:
        orders=[]
        order_total_info = { 'count': 0}
        items = []
        items_total_info= {'sum': 0, 'count': 0}
    glo = Global.get_instance()
    return {
        'items': items,
        'total_price': items_total_info['sum'],
        'total_count': items_total_info['count'],
        'nav_ad': nav_bar,
        'authors': authors,
        'orders': orders,
        'order_total_count': order_total_info['count'],
        'delivery_price': glo.delivery_price,
    }