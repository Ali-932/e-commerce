from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from ecommerce.home.models import nav_ad as NAV

def _common_base_View(request: HttpRequest,
                              ) -> dict:
    try:
        nav_ad = NAV.objects.get(active=True)
    except ObjectDoesNotExist:
        nav_ad = None
    return {
        'nav_ad': nav_ad,
    }

