from django.shortcuts import render
from ecommerce.abstract.utlites.menu_nums import menu_nums, DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.abstract.utlites.paginator import paginated_response, CustomPaginator
from ecommerce.abstract.utlites.search import get_search_results
from ecommerce.product.models import Volume, ProductBanner
from ecommerce.home.models import nav_ad as NAV


def list_products(request):
    per_page = int(request.GET.get('per_page', 12))
    page = int(request.GET.get('page', 1))
    pag=request.GET.get('pag',False)
    template = 'abstract/product/products_page.html'
    product_banner = 0 if request.htmx else ProductBanner.objects.filter(active=True).first()
    nav_bar = 0 if request.htmx else NAV.objects.get(active=True) # we only need the nav bar if we are refreshing the page
    volumes = Volume.objects.select_related('product').only('product__name',
                                                            'product__genres', 'product__themes',
                                                            'product__demographics', 'product__score',
                                                            'product__author',
                                                            'volume_number', 'price', 'image', 'start_chapter',
                                                            'end_chapter', 'price_currency',
                                                            )
    if request.htmx:
        if q:=request.GET.get('q',''):
            volumes = get_search_results(volumes, ['product__name'], q)
        if demo:=request.GET.get('demo',''):
            volumes = volumes.filter(product__demographics=[demo]) # the [] since the demo is an array field
        if theme:=request.GET.get('theme',''):
            volumes = volumes.filter(product__themes=[theme])
        if genre:=request.GET.get('genre',''):
            volumes = volumes.filter(product__genres=[genre])
        if sortby:=request.GET.get('sortby',''): # we get the 'sortby' value from the select value which corresponds to the field name
            volumes = volumes.order_by(sortby)
        if pag:
            offset = (page - 1) * per_page
            limit = offset + per_page
            volumes = volumes[offset:limit]

    menu_num = menu_nums.get('products',1)


    paginator = CustomPaginator(volumes, per_page)
    objs = paginator.page(page)

    demographics = {demo[0]: demo[1] for demo in DemographicChoices.choices} # we are using dict so we can get the database value and the display value
    themes = {theme[0]: theme[1] for theme in ThemeChoices.choices}
    genres = {genre[0]: genre[1] for genre in GenresChoices.choices}

    if volumes.__len__() == 0:
        template = 'abstract/product/empty_products.html'
    context = {
        'nav_ad': nav_bar,
        'menu_num': menu_num,
        'volumes': objs,
        'demographics': demographics,
        'themes': themes,
        'genres': genres,
        'pagination':paginated_response(volumes,per_page,page),
        'product_banner': product_banner,
    }

    return render(request, template, context)
