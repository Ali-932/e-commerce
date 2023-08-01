import contextlib

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import RedirectView

from ecommerce.abstract.utlites.base_function import _common_base_View
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.home.models import BModel, AModel, CModel, DModel
from ecommerce.home.models import nav_ad as NAV


class RootUrlView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        '''
        check if authenticated and redirect to the respective page accordingly
        '''
        return reverse('home:index') if self.request.user.is_authenticated else reverse('contact:login')


# @login_required
def index(request):
    models = [AModel, BModel, CModel, DModel]
    ads = []

    for model in models:
        try:
            ad = model.objects.get(active=True)
        except model.DoesNotExist:
            ad = None
        ads.append(ad)

    param = _common_base_View(request)
    template = 'abstract/index-20.html'
    menu_num = menu_nums.get('home',0)

    context = {
        'pretitle_url': reverse('home:index'),
        'adA': ads[0],
        'adB': ads[1],
        'adC': ads[2],
        'adD': ads[3],
        'nav_ad': param['nav_ad'],
        'menu_num': menu_num
    }

    if request.htmx:
        context['base'] = 'abstract/empty.html'
    else:
        context['base'] = 'abstract/_base.html'

    return render(request, template, context)

