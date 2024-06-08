from django.db.models import Q, F

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums, DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.abstract.utlites.paginator import paginated_response, CustomPaginator
from ecommerce.abstract.utlites.products.procces_form import process_form
from ecommerce.abstract.utlites.search import get_search_results
from ecommerce.product.froms.main_product_from import ProductForm
from ecommerce.product.models import Volume, ProductBanner, SpecialOfferProducts


def get_product_list_context(request, view_page='products'):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        volume, template = process_form(request, form,
                                        view_page, alternative_temp='abstract/product/product_list/products_page.html')
        common = common_views(request)
        context = {
            'volume': volume,
            'form': form,
            **common
        }
        return context, template

    per_page = int(request.GET.get('per_page', 12))
    page = int(request.GET.get('page', 1))
    pag = request.GET.get('pag', False)
    template = 'abstract/product/product_list/products_page.html'
    product_banner = ProductBanner.objects.filter(active=True).first()
    if view_page == 'products':
        volumes = Volume.objects.select_related('product').filter(product__type='Manga').only('product__name',
                                                                                              'product__genres',
                                                                                              'product__themes',
                                                                                              'product__demographics',
                                                                                              'product__score',
                                                                                              'product__author',
                                                                                              'volume_number', 'price',
                                                                                              'image', 'start_chapter',
                                                                                              'end_chapter',
                                                                                              'price_currency',
                                                                                              )
    elif view_page == 'special-offer':
        volumes = SpecialOfferProducts.objects.filter(is_available=True).values('volume__id')
        volumes = Volume.objects.filter(id__in=volumes).select_related('product').only(
            'product__name',
            'product__genres',
            'product__themes',
            'product__demographics',
            'product__score',
            'product__author',
            'volume_number',
            'image',
            'start_chapter',
            'end_chapter',
            'price_currency',
        ).annotate(
            discount_price=F('special_offer__price')
        ).annotate(
            language_available=F('special_offer__language')
        )

    author = None
    if request.htmx:
        filters = Q()
        if q := request.GET.get('q', ''):
            volumes = get_search_results(volumes, ['product__name'], q)
        if demo := request.GET.getlist('demo', ''):
            filters &= Q(product__demographics__overlap=demo)
        if theme := request.GET.getlist('theme', ''):
            filters &= Q(product__themes__overlap=theme)
        if genre := request.GET.getlist('genre', ''):
            filters &= Q(product__genres__overlap=genre)
        if sortby := request.GET.get('sortby',
                                     ''):  # we get the 'sortby' value from the select value which corresponds to the field name
            volumes = volumes.order_by(sortby)
        if author := request.GET.get('author', ''):
            author = author.split(' ')[0]
            filters &= Q(product__author__icontains=author)
        volumes = volumes.filter(filters)
        if pag:
            offset = (page - 1) * per_page
            limit = offset + per_page
            volumes = volumes[offset:limit]

    common = {} if request.htmx else common_views(request)
    if view_page == 'products':
        menu_num = menu_nums.get('products', 1)
    elif view_page == 'special-offer':
        menu_num = menu_nums.get('special-offers', 2)

    paginator = CustomPaginator(volumes, per_page)
    objs = paginator.page(page)

    demographics = {demo[0]: demo[1] for demo in
                    DemographicChoices.choices}  # we are using dict so we can get the database value and the display value
    themes = {theme[0]: theme[1] for theme in ThemeChoices.choices}
    genres = {genre[0]: genre[1] for genre in GenresChoices.choices}
    if volumes.__len__() == 0:
        template = 'abstract/product/product_list/empty_products.html'
    if view_page == 'products':
        title = 'جميع المنتجات'
    elif view_page == 'special-offer':
        title = 'عروض خاصة'
    context = {
        'title': title,
        'volumes': objs,
        'demographics': demographics,
        'themes': themes,
        'genres': genres,
        'pagination': paginated_response(volumes, per_page, page),
        'product_banner': product_banner,
        'form': form,
        'author': author,
        'menu_num': menu_num,
        **common
    }

    return context, template
