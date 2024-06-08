import contextlib

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Subquery, Count
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import RedirectView

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.home.models import BModel, AModel, CModel, DModel, VolumeABanner, VolumeBBanner
from ecommerce.home.models import nav_ad as NAV
from ecommerce.order.models import Order, OrderItem
from ecommerce.product.models import Volume


class RootUrlView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        '''
        check if authenticated and redirect to the respective page accordingly
        '''
        return reverse('home:index') if self.request.user.is_authenticated else reverse('contact:login')


# @login_required
def index(request):
    models = [AModel, BModel, CModel, DModel, VolumeABanner, VolumeBBanner]
    ads = []

    for model in models:
        try:
            ad = model.objects.get(active=True)
        except model.DoesNotExist:
            ad = None
        ads.append(ad)

    template = 'abstract/index-20.html'
    menu_num = menu_nums.get('home', 0)
    common = {} if request.htmx else common_views(request)
    best_sellers_volumes = Volume.objects.exclude(
        orderitem__order__status=Order.Status_CHOICES.PENDING).annotate(
        times_ordered=Count('orderitem')).order_by('-times_ordered')[:12]
    new_release = Volume.objects.order_by('-id')[:12]
    context = {
        'pretitle_url': reverse('home:index'),
        'adA': ads[0],
        'adB': ads[1],
        'adC': ads[2],
        'adD': ads[3],
        'volume_a_banner': ads[4],
        'volume_b_banner': ads[5],
        'menu_num': menu_num,
        'best_sellers': best_sellers_volumes,
        'new_release': new_release,
        **common
    }



    return render(request, template, context)


