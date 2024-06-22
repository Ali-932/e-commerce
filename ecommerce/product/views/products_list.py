from django.shortcuts import render
from django_ratelimit.decorators import ratelimit

from ecommerce.product.utils.list_products_utils import get_product_list_context
from ecommerce.settings import MEDIUM_REQUESTS_RATE_LIMIT, HEAVY_REQUESTS_RATE_LIMIT


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def list_products(request):
    context, template = get_product_list_context(request, 'products')

    return render(request, template, context)


@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def list_special_offer_products(request):
    context, template = get_product_list_context(request, 'special-offer')

    return render(request, template, context)

@ratelimit(key='ip', method='POST', rate=HEAVY_REQUESTS_RATE_LIMIT, block=True)
@ratelimit(key='ip', method='GET', rate=MEDIUM_REQUESTS_RATE_LIMIT, block=True)
def list_package_products(request):
    context, template = get_product_list_context(request, 'packages')

    return render(request, template, context)

