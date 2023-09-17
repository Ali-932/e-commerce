from django.db.models import Count, Max
from django.shortcuts import render
from ecommerce.abstract.utlites.menu_nums import menu_nums, DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.abstract.utlites.paginator import paginated_response, CustomPaginator
from ecommerce.abstract.utlites.search import get_search_results
from ecommerce.product.models import Volume
from ecommerce.home.models import nav_ad as NAV


def product(request, pk: int):
    template = 'abstract/product/product.html'
    nav_bar = 0 if request.htmx else NAV.objects.get(active=True) # we only need the nav bar if we are refreshing the page
    volume = Volume.objects.filter(pk=pk).select_related('product').annotate(
        total_volumes=Max('product__volume__volume_number')).first()
    next_volume = Volume.objects.filter(product=volume.product,
                                        pk=volume.pk + 1).first() if volume.volume_number <= volume.total_volumes else None
    prev_volume = Volume.objects.filter(product=volume.product,
                                        pk=volume.pk - 1).first() if volume.volume_number > 1 else None
    suggestions = Volume.objects.filter(product__genres__overlap=volume.product.genres).exclude(
        pk=volume.pk).select_related('product').order_by('?')[:4]
    menu_num = menu_nums.get('products',1)
    context = {
        'nav_ad': nav_bar,
        'menu_num': menu_num,
        'volume': volume,
        'next_volume': next_volume,
        'prev_volume': prev_volume,
        'volume_suggestions': suggestions,
    }
    return render(request, template, context)


