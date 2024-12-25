from django.contrib import messages
from django.db.models import Q, F, OuterRef, Subquery, Count
from django.db.models.functions import Coalesce

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.menu_nums import menu_nums, DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.abstract.utlites.paginator import paginated_response, CustomPaginator
from ecommerce.abstract.utlites.products.procces_form import process_form
from ecommerce.abstract.utlites.search import get_search_results
from ecommerce.product.froms.main_product_from import ProductForm
from ecommerce.product.models import Volume, ProductBanner, InventoryProduct, VolumesPackage


def get_product_list_context(request, view_page='products', category=None):
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            volume, template = process_form(request, form,
                                            alternative_temp='abstract/product/product_list/products_page.html')
            common = common_views(request)
            context = {
                'volume': volume,
                'form': form,
                **common
            }
            return context, template
        elif not form.is_valid():
            print(form.errors)
            messages.error(request, 'حدث خطا اثناء اضافة العنصر')

    per_page = int(request.GET.get('per_page', 12))
    page = int(request.GET.get('page', 1))
    pag = request.GET.get('pag', False)
    product_banner = ProductBanner.objects.filter(active=True).first()
    # items = Volume.objects.none()

    if view_page == 'products':
        items = Volume.objects.select_related('product').only('product__name',
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
        title = 'جميع المنتجات'

        if category:
            title = category[1]
            items = items.filter(product__type=category[0])
        # items = Volume.objects.all()
    elif view_page == 'special-offer':
        title = 'عروض خاصة'

        # sop_ids = InventoryProduct.objects.filter(is_available=True).values('id')
        items = InventoryProduct.objects.filter(is_available=True).select_related('product').only(
            'product__name',
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
    elif view_page == 'packages':
        title = 'حزمة المجلدات'
        items = VolumesPackage.objects.select_related('product').only(
            'product__name',
            'product__genres',
            'product__themes',
            'product__demographics',
            'product__score',
            'product__author',
            'volume_number', 'price',
            'image', 'start_volume',
            'end_volume',
            'price_currency',
            'volume_count'
        )
    author = None
    if request.htmx:
        filters = Q()
        if q := request.GET.get('q', ''):
            items = get_search_results(items, ['product__name'], q)
        if demo := request.GET.getlist('demo', ''):
            filters &= Q(product__demographics__overlap=demo)
        if theme := request.GET.getlist('theme', ''):
            filters &= Q(product__themes__overlap=theme)
        if genre := request.GET.getlist('genre', ''):
            filters &= Q(product__genres__overlap=genre)
        if sortby := request.GET.get('sortby',
                                     ''):  # we get the 'sortby' value from the select value which corresponds to the field name
            items = items.order_by(sortby)
        if author := request.GET.get('author', ''):
            author = author.split(' ')[0]
            filters &= Q(product__author__icontains=author)
        items = items.filter(filters)
        if pag:
            offset = (page - 1) * per_page
            limit = offset + per_page
            items = items[offset:limit]

    common = {} if request.htmx else common_views(request)
    if view_page == 'products':
        menu_num = menu_nums.get('products', 1)
    elif view_page == 'special-offer':
        menu_num = menu_nums.get('special-offers', 2)
    elif view_page == 'packages':
        menu_num = menu_nums.get('packages', 3)
    paginator = CustomPaginator(items, per_page)
    objs = paginator.page(page)

    demographics = {demo[0]: demo[1] for demo in
                    DemographicChoices.choices}  # we are using dict so we can get the database value and the display value
    themes = {theme[0]: theme[1] for theme in ThemeChoices.choices}
    genres = {genre[0]: genre[1] for genre in GenresChoices.choices}
    template = 'abstract/product/product_list/products_page.html'
    if items.__len__() == 0 and request.htmx:
        template = 'abstract/product/product_list/empty_products.html'
    context = {
        'title': title,
        'volumes': objs,
        'demographics': demographics,
        'themes': themes,
        'genres': genres,
        'pagination': paginated_response(items, per_page, page),
        'product_banner': product_banner,
        'form': form,
        'author': author,
        'menu_num': menu_num,
        **common
    }

    return context, template
