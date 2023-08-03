from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import _common_base_View
from ecommerce.abstract.utlites.menu_nums import menu_nums


def list_products(request):
    if request.htmx:
        base_template = 'abstract/empty.html'
    else:
        base_template = 'abstract/_base.html'
    menu_num = menu_nums.get('products',1)
    param = _common_base_View(request)

    context = {
        'base': base_template,
        'nav_ad': param['nav_ad'],
        'menu_num': menu_num
    }

    return render(request, 'abstract/product/products_page.html', context)
