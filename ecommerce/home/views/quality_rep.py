from django.shortcuts import render
from django.urls import reverse

from ecommerce.abstract.utlites.base_function import _common_base_View


def quality_page(request):
    if request.htmx:
        base_template = 'abstract/empty.html'
    else:
        base_template = 'abstract/_base.html'

    param = _common_base_View(request)

    return render(request, 'abstract/about/quality_rep.html', {
        'pretitle_url': reverse('home:index'),
        'base': base_template,
        'nav_ad': param['nav_ad'],
    })
