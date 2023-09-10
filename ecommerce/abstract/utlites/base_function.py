from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from ecommerce.home.models import nav_ad as NAV

def _common_base_View(request: HttpRequest,
                      model,
                      query,
                      # filters_callable: Callable,
                      *,
                      search_q: str,
                      extra_callable,
                      only_fields: list = None,
                      ) -> dict:

    per_page = int(request.GET.get('per_page', 10))
    page = int(request.GET.get('page', 1))
    q = request.GET.get('q', '')
    is_nav = request.GET.get('nav', False)
    if request.htmx and is_nav or not request.htmx:
        if only_fields:
            objs = query.only(*only_fields)
        try:
            nav_ad = NAV.objects.get(active=True)
        except ObjectDoesNotExist:
            nav_ad = None

    return nav_ad


