from django.shortcuts import render
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.home.models import nav_ad as NAV


def quality_page(request):
    menu_num = menu_nums.get('about',4)
    nav_bar = 0 if request.htmx else NAV.objects.get(active=True) # we only need the nav bar if we are refreshing the page

    context = {
        'base': 'base_template',
        'nav_ad': nav_bar,
        'menu_num': menu_num
    }

    return render(request, 'abstract/about/quality_rep.html', context)
