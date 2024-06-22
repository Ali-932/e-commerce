from django.db.models import OuterRef, Subquery, Count
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.abstract.utlites.products.procces_form import process_form
from ecommerce.product.froms.main_product_from import ProductForm
from ecommerce.product.models import Volume, VolumesPackage
from ecommerce.settings import MEDIUM_REQUESTS_RATE_LIMIT, HEAVY_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def package(request, pk: int):
    template = 'abstract/product/product_single/package.html'
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        volume, template, items, items_total_info = process_form(request, form, pk,
                                                                 'abstract/product/product_single/product.html',
                                                                 'abstract/product/product_list/product_view.html')
        context = {
            'volume': volume,
            'form': form,
            'items': items,
            'total_price': items_total_info['sum'],
            'total_count': items_total_info['count'],
        }

        return render(request, template, context)
    # main function for the view
    first_volume_number = Volume.objects.filter(
        package=OuterRef('pk')
    ).order_by('volume_number').values('volume_number')[:1]

    last_volume_number = Volume.objects.filter(
        package=OuterRef('pk')
    ).order_by('-volume_number').values('volume_number')[:1]
    item = VolumesPackage.objects.filter(pk=pk).select_related('product').annotate(
        start_volume=Coalesce(Subquery(first_volume_number), -1),
        end_volume=Coalesce(Subquery(last_volume_number), -1),
        total_volumes=Count('product__volume'),
    ).first()
    next_package = VolumesPackage.objects.filter(
        pk=pk + 1
    ).first() or None
    prev_package = VolumesPackage.objects.filter(
        pk=pk - 1
    ).first() or None
    package_volumes_count = item.volumes.count()
    suggestions = Volume.objects.filter(
        product__genres__overlap=item.product.genres
    ).exclude(pk=item.pk).select_related('product').order_by('?')[:4]
    common = {} if request.htmx else common_views(request)
    menu_num = menu_nums.get('package', 3)

    context = {
        'volume': item,
        'next_volume': next_package,
        'prev_volume': prev_package,
        'volume_suggestions': suggestions,
        'form': form,
        'menu_num': menu_num,
        'package_volumes_count': package_volumes_count,

        **common
    }

    return render(request, template, context)
