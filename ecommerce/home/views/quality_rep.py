from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.home.models import nav_ad as NAV


def quality_page(request):
    common = {} if request.htmx else common_views(request)
    menu_num = menu_nums.get('about', 4)

    context = {
        'menu_num': menu_num,
        **common,
    }

    return render(request, 'abstract/about/quality_rep.html', context)
