from django.contrib import messages

from ecommerce.home.views import index


def home_render_with_error(request, err_msg):
    messages.error(request, err_msg)
    return index(request)
