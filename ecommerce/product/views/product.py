from django.db.models import Max
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.abstract.utlites.products.procces_form import process_form
from ecommerce.product.froms.main_product_from import ProductForm
from ecommerce.product.models import Volume, Item
from ecommerce.settings import MEDIUM_REQUESTS_RATE_LIMIT, HEAVY_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def product(request, pk: int):
    template = 'abstract/product/product_single/product.html'
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        volume, template = process_form(request, form, pk,
                                        'abstract/product/product_single/product.html',
                                        'abstract/product/product_list/product_view.html')
        common = common_views(request)
        context = {
            'volume': volume,
            'form': form,
            **common
        }

        return render(request, template, context)
    # main function for the view

    volume = Item.objects.filter(pk=pk).select_related('product')
    next_volume = None
    prev_volume = None
    if volume.first().type in [
        Item.Type_CHOICES.Volume,
        Item.Type_CHOICES.InventoryProduct,
    ]:
        volume = volume.annotate(
            total_volumes=Max('product__volume__volume_number')).first()

        next_volume = Item.objects.filter(
            product=volume.product,
            pk=volume.pk + 1
        ).first() if volume.volume_number <= volume.total_volumes else None

        prev_volume = Item.objects.filter(
            product=volume.product,
            pk=volume.pk - 1
        ).first() if volume.volume_number > 1 else None

        all_volumes = Volume.objects.filter(product_id=volume.product_id).order_by('volume_number')
    else:
        volume = volume.annotate(total_volumes=Max('product__volume__volume_number'))
        volume = volume.first()
        all_volumes = volume.volumes.all().order_by('volume_number')
    suggestions = Item.objects.filter(
        product__genres__overlap=volume.product.genres
    ).exclude(pk=volume.pk).select_related('product').order_by('?')[:4]
    common = {} if request.htmx else common_views(request)
    menu_num = menu_nums.get('product', 1)
    context = {
        'volume': volume,
        'next_volume': next_volume,
        'prev_volume': prev_volume,
        'volume_suggestions': suggestions,
        'form': form,
        'menu_num': menu_num,
        'all_volumes': all_volumes,
        **common
    }

    return render(request, template, context)
