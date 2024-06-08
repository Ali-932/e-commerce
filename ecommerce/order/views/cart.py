from django.contrib import messages
from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check


def cart_page(request):
    if not request.user.is_authenticated:
        return permission_check(request)

    template = 'abstract/cart/cart.html'
    common = common_views(request)
    context = {
        **common,
    }
    return render(request, template, context)