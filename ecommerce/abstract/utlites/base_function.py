from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count
from django.http import HttpRequest

from ecommerce.home.models import nav_ad as NAV
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
from ecommerce.order.models import OrderItem
from ecommerce.product.models import Volume


def common_views(request):
    menu_num = menu_nums.get('products', 1)
    orders= OrderItem.objects.select_related('volume','order').filter(order__user=request.user,order__active=True)
    total_info=orders.aggregate(sum=Sum('price'),count=Count('id'))
    nav_bar = 0 if request.htmx else NAV.objects.get(active=True) # we only need the nav bar if we are refreshing the page
    authors = Volume.objects.filter(
        product__score__gt=8.9).distinct(
        'product__author').values('product__author')[:10]
    authors = [list(item['product__author'].keys())[0] for item in authors]
    return menu_num, orders, total_info, nav_bar, authors