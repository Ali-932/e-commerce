from django.db.models import Prefetch
from django.shortcuts import render
from django.template.loader import render_to_string

from ecommerce.abstract.utlites.base_function import _common_base_View
from ecommerce.abstract.utlites.menu_nums import menu_nums, DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.abstract.utlites.paginator import paginated_response, CustomPaginator
from ecommerce.abstract.utlites.search import get_search_results
from ecommerce.product.models import Volume
from ecommerce.home.models import nav_ad as NAV


def list_products(request):
    per_page = int(request.GET.get('per_page', 12))
    page = int(request.GET.get('page', 1))
    pag=request.GET.get('pag',False)
    template = 'abstract/product/products_page.html'
    nav_bar=0
    if not request.htmx:
        volumes = Volume.objects.select_related('product').only('product__name',
                                                                'product__genres', 'product__themes',
                                                                'product__demographics', 'product__score','product__author',
                                                                'volume_number', 'price', 'image', 'start_chapter',
                                                                'end_chapter', 'price_currency',
                                                                )

        nav_bar = NAV.objects.get(active=True)

    else:
        q=request.GET.get('q','')
        if pag:
            offset = (page - 1) * per_page
            limit = offset + per_page
            volumes = Volume.objects.select_related('product').only('product__name',
                                                                    'product__genres', 'product__themes',
                                                                    'product__demographics', 'product__score',
                                                                    'volume_number', 'price', 'image', 'start_chapter',
                                                                    'end_chapter', 'price_currency',
                                                                    )
            volumes = get_search_results(volumes, ['product__name'], q)[offset:limit]

        else:
            volumes = Volume.objects.select_related('product').only('product__name',
                                                                'product__genres', 'product__themes',
                                                                'product__demographics', 'product__score',
                                                                'volume_number', 'price', 'image', 'start_chapter',
                                                                'end_chapter', 'price_currency',
                                                                )
            volumes = get_search_results(volumes, ['product__name'], q)

    menu_num = menu_nums.get('products',1)


    paginator = CustomPaginator(volumes, per_page)
    objs = paginator.page(page)

    demographics = {demo[0]: demo[1] for demo in DemographicChoices.choices}
    themes = {theme[0]: theme[1] for theme in ThemeChoices.choices}
    genres = {genre[0]: genre[1] for genre in GenresChoices.choices}
    context = {
        'nav_ad': nav_bar,
        'menu_num': menu_num,
        'volumes': objs,
        'demographics': demographics,
        'themes': themes,
        'genres': genres,
        'pagination':paginated_response(volumes,per_page,page),
    }

    return render(request, template, context)
