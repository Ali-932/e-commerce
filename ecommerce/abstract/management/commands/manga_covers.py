from django.core.management.base import BaseCommand
from ecommerce.product.models import *
import os
from ecommerce.settings import MEDIA_ROOT


def find_cover_path(id):
    cover_root = os.path.join(MEDIA_ROOT, 'images/covers')
    for filename in os.listdir(cover_root):
        name, ext = os.path.splitext(filename)
        if name == str(id):
            file_path = os.path.join(cover_root, filename)
            print(f"Found file: {file_path}")
            file_path = os.path.join('images/covers', filename)
            print(file_path)
            return file_path


class Command(BaseCommand):
    def handle(self, *args, **options):
        items = Volume.objects.filter(image__icontains='mangadex').values('id')
        for item in items:
            cover_path = find_cover_path(item['id'])
            print(cover_path)
            if cover_path:
                volume = Volume.objects.get(id=item['id'])
                volume.image = cover_path
                volume.save()
