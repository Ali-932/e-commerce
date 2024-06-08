from django.db.models import Max
from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums
from ecommerce.abstract.utlites.products.procces_form import process_form
from ecommerce.product.froms.main_product_from import ProductForm
from ecommerce.product.models import Volume


def product(request, pk: int):
    template = 'abstract/product/product_single/product.html'
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        volume, template, items, items_total_info = process_form(request, form, pk,
                                                                 'abstract/product/product_single/product.html',
                                                                 'abstract/product/product_single/product_view.html')
        context = {
            'volume': volume,
            'form': form,
            'items': items,
            'total_price': items_total_info['sum'],
            'total_count': items_total_info['count'],
        }

        return render(request, template, context)

    # main function for the view
    volume = Volume.objects.filter(pk=pk).select_related('product').annotate(
        total_volumes=Max('product__volume__volume_number')).first()

    next_volume = Volume.objects.filter(
        product=volume.product,
        pk=volume.pk + 1
    ).first() if volume.volume_number <= volume.total_volumes else None

    prev_volume = Volume.objects.filter(
        product=volume.product,
        pk=volume.pk - 1
    ).first() if volume.volume_number > 1 else None

    suggestions = Volume.objects.filter(
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
        **common
    }

    return render(request, template, context)
