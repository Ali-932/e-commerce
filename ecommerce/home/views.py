import contextlib

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import RedirectView

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
    try:
        nav_ad = NAV.objects.get(active=True)
    except ObjectDoesNotExist:
        nav_ad = None

    return render(request, 'abstract/index-20.html', {
        'pretitle_url': reverse('home:index'),
        'adA': ads[0],
        'adB': ads[1],
        'adC': ads[2],
        'adD': ads[3],
        'nav_ad': nav_ad,
    })

