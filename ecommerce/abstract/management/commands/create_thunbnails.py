import re

from django.core.management.base import BaseCommand
from ecommerce.product.models import *
import os
from ecommerce.settings import MEDIA_ROOT


def find_cover_path(file_name):
    cover_root = '/home/james/PycharmProjects/e-commerce/media/images/covers'
    for filename in os.listdir(cover_root):
        name, ext = os.path.splitext(filename)
        sanitized_new_file_name = sanitize_filename(file_name)
        if name == str(sanitized_new_file_name) or name == str(file_name):
            file_path = os.path.join(cover_root, filename)
            print(f"Found file: {file_path}")
            file_path = os.path.join('/home/james/PycharmProjects/e-commerce/media/images/covers', filename)
            return file_path


def sanitize_filename(filename):
    # Regular expression to remove invalid characters
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

class Command(BaseCommand):
    def handle(self, *args, **options):
        items = Item.objects.filter(thumbnail__isnull=True)
        print(items)
        for item in items:
            try:
                print(item.image)
                image = Image.open(item.image)
                print(image)
            except FileNotFoundError:
                print(f"File not found: {item.image}")
                cover_path = find_cover_path(f'{item.product.name} - {item.volume_number}')
                print(cover_path)
                if cover_path is None:
                    raise ValueError(f"File not found: {item.product.name} - {item.volume_number}")
                real_path = os.path.relpath(cover_path, "/home/james/PycharmProjects/e-commerce/media")
                with Image.open(cover_path) as img:
                    image_io = BytesIO()
                    img.save(image_io, format=img.format)
                    item.image.save(real_path, File(image_io), save=True)
                    image = Image.open(item.image)

            image = image.convert('RGB')
            # Define the size
            size = (300, 300)
            image.thumbnail(size, Image.LANCZOS)
            print('here')

            thumb_io = BytesIO()
            image.save(thumb_io, 'JPEG', quality=85)

            thumbnail = File(thumb_io, name=os.path.basename(item.image.name))
            print()
            item.thumbnail.save(thumbnail.name, thumbnail, save=False)
            item.save()


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
