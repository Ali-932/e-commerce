from django.shortcuts import render

from ecommerce.abstract.utlites.base_function import common_views
from ecommerce.abstract.utlites.permission_check import permission_check


def view_orders(request):
    if not request.user.is_authenticated:
        return permission_check(request)

    template='abstract/order/orders.html'
    common = common_views(request)

    context = {
        **common,
    }

    return render(request,template,context)