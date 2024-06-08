from django.shortcuts import render

from ecommerce.product.utils.list_products_utils import get_product_list_context


def list_products(request):

    context, template = get_product_list_context(request, 'products')

    return render(request, template, context)

def list_special_offer_products(request):
    context, template = get_product_list_context(request, 'special-offer')

    return render(request, template, context)