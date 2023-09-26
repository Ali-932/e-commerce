from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.home.models import nav_ad as NAV


def quality_page(request):
    menu_num, orders, total_info, nav_bar, authors = common_views(request)

    context = {
    'nav_ad': nav_bar,
    'menu_num': menu_num,
    'orders':orders,
    'total_price':total_info['sum'],
    'total_count':total_info['count'],
    'authors': authors
    }

    return render(request, 'abstract/about/quality_rep.html', context)
