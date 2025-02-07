from django.urls import reverse
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from ecommerce.product.utils.list_products_utils import get_product_list_context
from ecommerce.settings import MEDIUM_REQUESTS_RATE_LIMIT, LIGHT_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=LIGHT_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
# @cache_page(60 * 15)  # Cache for 15 minutes
def list_products(request):
    path_to_category = {
        reverse('product:list-products-manga'): ('Manga', 'المانجا'),
        reverse('product:list-products-manhwa'): ('Manhwa', "المانهوا"),
        reverse('product:list-products-comic'): ('Comic', "الكوميك")
    }

    category = path_to_category.get(request.path, None)
    response = get_product_list_context(request, 'products', category)

    return response


@ratelimit(key='ip', method='POST', rate=LIGHT_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def list_special_offer_products(request):
    response = get_product_list_context(request, 'special-offer')

    return response


@ratelimit(key='ip', method='POST', rate=LIGHT_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def list_package_products(request):
    response = get_product_list_context(request, 'packages')

    return response
