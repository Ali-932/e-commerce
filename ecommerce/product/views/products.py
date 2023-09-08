from django.db.models import Prefetch
from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import _common_base_View
from ecommerce.abstract.utlites.menu_nums import menu_nums, DemographicChoices
from ecommerce.abstract.utlites.paginator import paginated_response, CustomPaginator
from ecommerce.abstract.utlites.search import get_search_results
from ecommerce.product.models import Volume


def list_products(request):
    nav_bar=0
    per_page = int(request.GET.get('per_page', 12))
    page = int(request.GET.get('page', 1))
    is_nav = request.GET.get('nav', False)
    if request.htmx and is_nav or not request.htmx:
        template = 'abstract/product/products_page.html'
        volumes = Volume.objects.select_related('product').only('product__name',
                                                                'product__genres', 'product__themes',
                                                                'product__demographics', 'product__score','product__author',
                                                                'volume_number', 'price', 'image', 'start_chapter',
                                                                'end_chapter', 'price_currency',
                                                                )

        nav_bar = _common_base_View(request)

    else:
        template = 'abstract/product/list-product.html'
        offset = (page - 1) * per_page
        limit = offset + per_page
        q=request.GET.get('q','')
        volumes = Volume.objects.select_related('product').only('product__name',
                                                                'product__genres', 'product__themes',
                                                                'product__demographics', 'product__score',
                                                                'volume_number', 'price', 'image', 'start_chapter',
                                                                'end_chapter', 'price_currency',
                                                                ).filter(product__name__icontains=q)[offset:limit]
        # if q := request.GET.get('q', ''):
        #     volumes = get_search_results(volumes, ['product__name'], q)

    menu_num = menu_nums.get('products',1)


    paginator = CustomPaginator(volumes, per_page)
    objs = paginator.page(page)

    demographics = [demo[0] for demo in DemographicChoices.choices]
    context = {
        'nav_ad': nav_bar,
        'menu_num': menu_num,
        'volumes': objs,
        'demographics': demographics,
        'pagination':paginated_response(volumes,per_page,page),
    }

    return render(request, template, context)
