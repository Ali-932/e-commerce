# ecommerce/middleware.py

from django.utils import translation
from django.conf import settings

class AdminEnglishMiddleware:
    """
    Middleware to force the admin interface to use English,
    while keeping the rest of the site in the default language.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the admin interface
        if request.path.startswith(f'/{settings.ADMIN_URL}'):
            # Activate English for admin
            translation.activate('en')
            request.LANGUAGE_CODE = 'en'
        else:
            # Activate the default language (Arabic)
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE

        response = self.get_response(request)

        # Deactivate the current translation after the response
        translation.deactivate()

        return response