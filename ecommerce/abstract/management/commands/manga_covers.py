import re

from django.core.management.base import BaseCommand
from ecommerce.product.models import *
import os
from ecommerce.settings import MEDIA_ROOT


def find_cover_path(file_name):
    cover_root = os.path.join(MEDIA_ROOT, 'images/covers')
    for filename in os.listdir(cover_root):
        name, ext = os.path.splitext(filename)
        sanitized_new_file_name = sanitize_filename(file_name)
        if name == str(sanitized_new_file_name):
            file_path = os.path.join(cover_root, filename)
            print(f"Found file: {file_path}")
            file_path = os.path.join('images/covers', filename)
            print(file_path)
            return file_path


def sanitize_filename(filename):
    # Regular expression to remove invalid characters
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


class Command(BaseCommand):
    def handle(self, *args, **options):
        items = Volume.objects.values('id', 'volume_number', 'product__name')
        for item in items:
            print(item)
            cover_path = find_cover_path(f'{item["product__name"]} - {item["volume_number"]}')
            # if cover_path:
            #     rename_cover(cover_path, f'{item["product__name"]} - {item["volume_number"]}')
            if cover_path:
                volume = Volume.objects.get(id=item['id'])
                volume.image = cover_path
                volume.save()

### Archive
## Used to change the name of the manga covers from ids to manga name and volume number
# def rename_cover(path, new_filename):
#     print(path)
#     path = '/home/james/PycharmProjects/e-commerce/media/' + path
#     print(path)
#     directory = os.path.dirname(path)
#     sanitized_new_file_name = sanitize_filename(new_filename)
#     new_file_path = os.path.join(directory, sanitized_new_file_name)
#     exe = path.split('.')[-1]
#     os.rename(path, new_file_path+'.'+exe)
