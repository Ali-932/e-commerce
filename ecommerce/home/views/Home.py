from django.db.models import Count
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.views.generic import RedirectView
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.home.models import BModel, AModel, CModel, DModel, VolumeABanner, VolumeBBanner
from ecommerce.order.models import Order
from ecommerce.product.froms.main_product_from import ProductForm
from ecommerce.product.models import Volume, Item
from ecommerce.settings import LIGHT_REQUESTS_RATE_LIMIT


class RootUrlView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        '''
        check if authenticated and redirect to the respective page accordingly
        '''
        return reverse('home:index') if self.request.user.is_authenticated else reverse('contact:login')


# @login_required
@ratelimit(key='ip', method='GET', rate=LIGHT_REQUESTS_RATE_LIMIT, block=True)
def index(request):
    models = [AModel, BModel, CModel, DModel, VolumeABanner, VolumeBBanner]
    ads = []
    form = ProductForm(request.POST or None)

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
    new_release = Item.objects.order_by('-id')[:12]

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
        'form': form,
        **common
    }

    return render(request, template, context)
