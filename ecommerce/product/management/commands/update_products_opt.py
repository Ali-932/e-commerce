import ast
import json
import os
import random
import re
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from io import BytesIO
import multiprocessing

import requests
from PIL import Image
from django.core.cache import cache
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from fuzzywuzzy import fuzz
from translatepy.translators.google import GoogleTranslate
from tqdm import tqdm

from ecommerce.abstract.utlites.menu_nums import DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.product.models import Product, Volume, InventoryProduct

# Initialize translator
translator = GoogleTranslate()

# Constants
BATCH_SIZE = 50
MAX_WORKERS = multiprocessing.cpu_count() * 2
IMAGE_DOWNLOAD_TIMEOUT = 30
COVER_ROOT = 'covers'
SIMILARITY_THRESHOLD = 85


class ImageProcessor:
    @staticmethod
    def sanitize_filename(filename):
        return re.sub(r'[<>:"♥/\\|?*]', '_', filename)

    @staticmethod
    def create_output_directory(base_dir):
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    @staticmethod
    def download_image(session, url, output_dir, image_id):
        try:
            response = session.get(url, timeout=IMAGE_DOWNLOAD_TIMEOUT, )
            response.raise_for_status()

            filename = ImageProcessor.sanitize_filename(str(image_id))
            content_type = response.headers.get('Content-Type', '')
            ext = content_type.split('/')[-1] if content_type else 'jpg'
            filename = f"{filename}.{ext}"

            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True, filepath
        except Exception as e:
            print(f"Error downloading image {url}: {str(e)}")
            return False, None

    @staticmethod
    def batch_process_images(image_batch):
        ImageProcessor.create_output_directory(COVER_ROOT)
        results = []

        with requests.Session() as session:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = [
                    executor.submit(
                        ImageProcessor.download_image,
                        session,
                        image_url,
                        COVER_ROOT,
                        f"{product_name} - {volume_num}"

                    )
                    for image_url, product_name, volume_num in image_batch
                ]
                results = [f.result() for f in futures]

        return results


class TranslationService:
    @staticmethod
    @lru_cache(maxsize=1000)
    def translate(text, dest_lang='arabic', source_lang='english'):
        if not text:
            return None

        cache_key = f"trans_{hash(text)}_{dest_lang}_{source_lang}"
        result = cache.get(cache_key)

        if result is None:
            result = translator.translate(
                text,
                destination_language=dest_lang,
                source_language=source_lang
            )
            cache.set(cache_key, result, timeout=86400)  # Cache for 24 hours

        return result


class ProductService:
    @staticmethod
    def find_similar_products(titles, threshold=SIMILARITY_THRESHOLD):
        all_products = list(Product.objects.values(
            'id', 'name', 'title_english', 'title_japanese'
        ))
        similar_products = []
        title_set = {title.lower() for title in titles if title}

        for product in all_products:
            product_titles = {
                product['name'].lower(),
                product['title_english'].lower() if product['title_english'] else '',
                product['title_japanese'].lower() if product['title_japanese'] else ''
            }

            if any(fuzz.ratio(t1, t2) >= threshold
                   for t1 in title_set
                   for t2 in product_titles if t2):
                similar_products.append(product)

        return similar_products

    @staticmethod
    def prepare_volume(volume_data, product, language):
        if 'image_url' not in volume_data or not volume_data['image_url']:
            volume_data['image_url'] = 'https://i.ibb.co/82Fb1DC/47b000fb-c5af-451a-a6b2-580e7b4c81bc-copy.png'

        return {
            'product': product,
            'volume_number': volume_data['volume'],
            'price': 8000,
            'image_url': volume_data['image_url'],
            'start_chapter': volume_data['start_chapter'],
            'end_chapter': volume_data['end_chapter'],
            'language': language
        }


class Command(BaseCommand):
    help = "Import manga data with optimized performance"

    def add_arguments(self, parser):
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        with open('ecommerce/product/management/commands/fixtures/manga_data4.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load progress
        progress = self.load_progress()
        start_index = progress.get('last_index', 0)

        # Process in batches
        for batch_start in tqdm(range(start_index, len(data), BATCH_SIZE)):
            batch_end = min(batch_start + BATCH_SIZE, len(data))
            batch = data[batch_start:batch_end]

            try:
                self.process_batch(batch)
                self.save_progress({'last_index': batch_end})
            except Exception as e:
                print(f"Error processing batch {batch_start}-{batch_end}: {str(e)}")
                self.save_progress({'last_index': batch_start})
                raise

    def process_batch(self, batch):
        volumes_to_create = []
        image_batch = []

        for item in batch:
            if self.should_skip_item(item):
                continue

            authors = self.process_authors(item)
            if not authors:
                continue

            product = self.process_product(item, authors)
            if not product:
                continue

            volumes = self.prepare_volumes(item, product)
            volumes_to_create.extend(volumes)

            # Collect image information for batch processing
            for vol in volumes:
                image_batch.append((
                    vol['image_url'],
                    product.name,
                    vol['volume_number']
                ))

        # Batch process images
        image_results = ImageProcessor.batch_process_images(image_batch)

        # Create volumes with processed images
        self.create_volumes_batch(volumes_to_create, image_results)

    def should_skip_item(self, item):
        if 'Colored'.lower() in item['title'].lower():
            return True

        if not item['start_date'] or item['start_date'] == "Unknown":
            return True

        date_to_match = int(item['start_date'][:4] if len(item['start_date']) > 4 else item['start_date'])
        return date_to_match < 2010

    def process_authors(self, item):
        try:
            authors_list = json.loads(item['authors'].replace("'", '"'))
            if 'first_name' not in authors_list[0]:
                return None

            authors = {}
            for author in authors_list:
                name = f"{author['first_name']} {author['last_name']}"
                name_ar = TranslationService.translate(name)
                authors[name_ar] = author.get('role', 'القصة والفن')

            return authors
        except Exception as e:
            print(f"Error processing authors: {str(e)}")
            return None

    def process_product(self, item, authors):
        genres, demo, synonyms, themes = map(
            ast.literal_eval,
            (item['genres'], item['demographics'], item['title_synonyms'], item['themes'])
        )

        demo_ar = [choice[0] for choice in DemographicChoices.choices
                   if any(d and d.lower() == choice[1].lower() for d in demo)]
        genres_ar = [choice[0] for choice in GenresChoices.choices
                     if any(g and g.lower() == choice[1].lower() for g in genres)]
        themes_ar = [choice[0] for choice in ThemeChoices.choices
                     if any(t and t.lower() == choice[1].lower() for t in themes)]

        product_titles = [item['title'], item['title_japanese'], item['title_english']] + synonyms
        similar_products = ProductService.find_similar_products(product_titles)

        if similar_products:
            return Product.objects.get(id=similar_products[0]['id'])

        return self.create_new_product(item, authors, demo_ar, genres_ar, themes_ar, synonyms)

    def create_new_product(self, item, authors, demo_ar, genres_ar, themes_ar, synonyms):
        synopsis_ar = TranslationService.translate(item['synopsis'])
        background_ar = TranslationService.translate(item['background'])
        title_ar = TranslationService.translate(item['title'])

        score = item['score']
        if score is None or score > 6:
            score = round(random.uniform(1, 5), 2)

        return Product.objects.create(
            name=ImageProcessor.sanitize_filename(item['title']),
            type='Manga',
            genres=genres_ar,
            themes=themes_ar,
            demographics=demo_ar,
            synopsis=synopsis_ar,
            background=background_ar,
            start_date=f"{item['start_date']}-1-1",
            end_date=item['end_date'],
            score=score,
            favorites=item['favorites'],
            title_japanese=item['title_japanese'],
            title_english=item['title_english'],
            title_arabic=title_ar,
            title_synonyms=synonyms,
            author=authors
        )

    def prepare_volumes(self, item, product):
        language = (InventoryProduct.Language_CHOICES.BOTH
                    if ProductService.find_similar_products([item['title']]) or int(item['start_date']) > 2022
                    else InventoryProduct.Language_CHOICES.EN)

        volumes = []
        for volume in item['volumes']:
            try:
                volume_number = int(volume['volume'])
                volumes.append(ProductService.prepare_volume(volume, product, language))
            except ValueError:
                continue

        return volumes

    @staticmethod
    def create_volumes_batch(volumes_to_create, image_results):
        volume_objects = []

        for volume, (success, image_path) in zip(volumes_to_create, image_results):
            if success and image_path:
                with Image.open(image_path) as img:
                    image_io = BytesIO()
                    img.save(image_io, format=img.format)
                    image_io.seek(0)
                    volume['image'] = File(image_io, name=os.path.basename(image_path))
                    image_url = volume.pop('image_url')
                    volume_objects.append(Volume(**volume))

        Volume.objects.bulk_create(volume_objects, batch_size=100)

    @staticmethod
    def load_progress():
        try:
            with open('import_progress.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'last_index': 0}

    @staticmethod
    def save_progress(progress):
        with open('import_progress.json', 'w') as f:
            json.dump(progress, f)
