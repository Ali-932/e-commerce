from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.urls import reverse

from ecommerce.home.models import *
from ecommerce.product.models import VolumesPackage, Product, Volume

from translatepy.translators.google import GoogleTranslateV2 as GoogleTranslate

translator = GoogleTranslate()

class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.filter(title_english__isnull=False, title_arabic__isnull=True)
        for product in products:
            if product.title_english:
                product.title_arabic = translator.translate(product.title_english, destination_language='arabic',source_language='english')
                product.save()

