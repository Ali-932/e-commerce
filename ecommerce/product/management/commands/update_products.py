import ast
import json
import os
import random
import re
from io import BytesIO

import requests
from PIL import Image
from django.core.files import File
from django.core.management.base import BaseCommand
from fuzzywuzzy import fuzz
from translatepy.translators.google import GoogleTranslateV2 as GoogleTranslate

from ecommerce.abstract.utlites.menu_nums import DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.product.models import Product, Volume, InventoryProduct
from django.core.management.base import CommandError
import time
translator = GoogleTranslate()


def save_progress(index):
    with open('import_progress.json', 'w') as f:
        json.dump({'last_processed_index': index}, f)

def load_progress():
    try:
        with open('import_progress.json', 'r') as f:
            data = json.load(f)
            return data.get('last_processed_index', -1)
    except FileNotFoundError:
        return -1

def are_titles_similar(title1, title2, threshold=85):
    # Returns True if titles are similar enough based on the threshold
    ratio = fuzz.ratio(title1.lower(), title2.lower())
    return ratio >= threshold


def find_similar_products(titles, threshold=85):
    # Get all products from database
    all_products = Product.objects.all()

    similar_products = []

    for product in all_products:
        for title in titles:
            if any([
                are_titles_similar(title, product.name, threshold),
                are_titles_similar(title, product.title_english, threshold) if product.title_english else None,
                are_titles_similar(title, product.title_japanese, threshold) if product.title_japanese else None,
            ]):
                similar_products.append({
                    'id': product.id,
                    'name': product.name,
                    'title_english': product.title_english,
                    'title_japanese': product.title_japanese,
                    'similarity_match': title  # The title that matched
                })
                break

    return similar_products


def sanitize_filename(filename):
    # Regular expression to remove invalid characters
    return re.sub(r'[<>:"♥/\\|?*]', '_', filename)


def find_cover_path(file_name):
    cover_root = os.path.join('covers')
    for filename in os.listdir(cover_root):
        name, ext = os.path.splitext(filename)
        sanitized_new_file_name = sanitize_filename(file_name)
        if name == str(sanitized_new_file_name):
            file_path = os.path.join(cover_root, filename)
            print(f"Found file: {file_path}")
            return file_path


def download_image(session, url, output_dir, image_id):
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        filename = f"{image_id}"
        filename = sanitize_filename(filename)
        content_type = response.headers.get('Content-Type')
        if content_type:
            ext = content_type.split('/')[-1]
            filename += f".{ext}"
        else:
            filename += ".jpg"  # Default extension
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True, url
    except Exception as e:
        raise (e)


def create_output_directory(base_dir):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)


class Command(BaseCommand):
    help = "upload accounts (create COA)"
    MAX_RETRIES = 300
    RETRY_DELAY = 3  # seconds
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        retries = self.MAX_RETRIES
        delay = self.RETRY_DELAY
        attempt = 0
        while attempt < retries:
            try:
                self.process_data(*args, **options)
                break  # If successful, exit the loop
            except Exception as e:
                attempt += 1
                print(e)
                if attempt >= retries:
                    raise CommandError(f"Failed after {retries} attempts. Last error: {str(e)}")

                self.stdout.write(
                    self.style.WARNING(
                        f"Attempt {attempt} failed: {str(e)}. Retrying in {delay} seconds..."
                    )
                )
                time.sleep(delay)


    def process_data(self, *args, **options):
        with open('ecommerce/product/management/commands/fixtures/manga_data4.json', 'r', encoding='utf-8') as f:
            jsonf = json.load(f)

            # Load the last processed index
            start_index = load_progress() + 1

            # Process items starting from the last saved position
            for index in range(start_index, len(jsonf)):
                try:
                    i = jsonf[index]
                    self.stdout.write(f'Processing item {index + 1} of {len(jsonf)}')

                    if 'Colored'.lower() in i['title'].lower():
                        self.stdout.write('manga is colored !!')
                        continue

                    if 'Anthology'.lower() in i['title'].lower():
                        self.stdout.write('manga is anthology !!')
                        continue

                    self.handel_authers(i)

                    # Save progress after each successful processing
                    save_progress(index)
                except json.decoder.JSONDecodeError as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing item {index}: {str(e)}")
                    )
                    continue
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing item {index}: {str(e)}")
                    )
                    # Save progress even if there's an error
                    save_progress(index - 1)
                    raise e
    def handel_authers(self, i):
        print(f'passed {i["title"]}')
        # print(len(i['start_date']))
        # print(i['start_date'][:4])
        if 'Colored'.lower() in i['title'].lower():
            print('manga is colored !!')
            return
        if i['start_date'] is None or i['start_date'] == "Unknown":
            print(f'{i["title"]} manga has no start date')
            return
        elif len(i['start_date']) > 4:
            date_to_match = int(i['start_date'][:4])
        else:
            date_to_match = int(i['start_date'])
        if date_to_match < 2010:
            print(f'{i["title"]} manga is older than 2010s')
            return
        try:
            checking_score = float(i['score'])
            print(checking_score)
        except Exception as e:
            print(f'{i["title"]} manga has no score')
            return
        if checking_score <= 8:
            print(f'{i["title"]} manga has a bad score')
            return
        if (len(i['title'].strip("<>:♥/\\|?*"))) > 200:
            return

        # print(i['title'])
        str_list = i['authors']
        str_list = str_list.replace("'", '"')
        list_obj = json.loads(str_list)
        au = {}
        if 'first_name' not in list_obj[0]:
            return
        for author in list_obj:
            first = author['first_name']
            last = author['last_name']
            name = f'{first} {last}'
            # print(name)
            name = translator.translate(name, destination_language='arabic', source_language='english')
            # print(name)
            au[f'{name}'] = author.get('role', 'القصة والفن')
        self.handel_product(i, au)

    def handel_product(self, i, au):
        genres, demo, title_synonyms, themes = map(
            ast.literal_eval, (i['genres'],
                               i['demographics'],
                               i['title_synonyms'], i['themes']))
        demo_ar = []
        genres_ar = []
        themes_ar = []
        for de in demo:
            if de:
                demo_ar.extend(
                    choices[0]
                    for choices in DemographicChoices.choices
                    if choices[1].lower() == de.lower()
                )
        for gen in genres:
            if gen:
                genres_ar.extend(
                    choices[0]
                    for choices in GenresChoices.choices
                    if choices[1].lower() == gen.lower()
                )
        for theme in themes:
            if theme:
                themes_ar.extend(
                    choices[0]
                    for choices in ThemeChoices.choices
                    if choices[1].lower() == theme.lower()
                )
        start_date = f"{i['start_date']}-1-1"
        product_titles = [i['title'], i['title_japanese'], i['title_english']]
        product_titles.extend(title_synonyms)
        similar_products = find_similar_products(product_titles)
        product_exists = len(similar_products) > 0
        # print({
        #     'title': i['title'],
        #     'title_japanese': i['title_japanese'],
        #     'title_english': i['title_english'],
        #     'synopsis': i['synopsis'],
        #     'exist:': product_exists,
        #     'similar_products': similar_products
        # })
        # print('-=====================')
        if product_exists or int(i['start_date']) > 2022:
            language = InventoryProduct.Language_CHOICES.BOTH
        else:
            language = InventoryProduct.Language_CHOICES.EN
        # print(i['start_date'])
        # print(language)
        # print(demo_ar)
        if product_exists:
            po = Product.objects.get(id=similar_products[0]['id'])
        else:
            synopsis_ar = translator.translate(i['synopsis'], destination_language='arabic',
                                               source_language='english') if i['synopsis'] else None
            background_ar = translator.translate(i['background'], destination_language='arabic',
                                                 source_language='english') if i['background'] else None
            title_arabic = translator.translate(i['title'], destination_language='arabic', source_language='english')
            score = i['score']
            if score is None:
                random_float = random.uniform(1, 5)
                rounded_float = round(random_float, 2)
                score = rounded_float
            elif score > 7:
                random_float = random.uniform(1, 2)
                rounded_float = round(random_float, 2)
                score -= rounded_float
            po, _ = Product.objects.get_or_create(
                name=i['title'].strip("<>:♥/\\|?*"),
                type='Manga',
                genres=genres_ar,
                themes=themes_ar,
                demographics=demo_ar,
                synopsis=synopsis_ar,
                background=background_ar,
                start_date=start_date,
                end_date=i['end_date'],
                score=score,
                favorites=i['favorites'],
                title_japanese=i['title_japanese'],
                title_english=i['title_english'],
                title_arabic=title_arabic,
                title_synonyms=title_synonyms,
                author=au
            )
        # print(po)
        self.handel_volumes(po, i, product_exists, language)

    def handel_volumes(self, po, i, product_exists, language):
        if product_exists:
            existing_volumes = list(
                Volume.objects.filter(product=po).order_by('volume_number').values_list('volume_number', flat=True))
            # print(f'existing volumes in the db are {existing_volumes}')
            # print(f'volumes in the json are {[volume["volume"] for volume in i["volumes"]]}')
            for volume in i['volumes']:
                try:
                    volume_number = int(volume['volume'])
                except Exception as e:
                    print(f'volume number is not a interger, skipping')
                    continue
                if volume_number not in existing_volumes:
                    create_volume(volume, po, language)

        else:
            for volume in i['volumes']:
                try:
                    _ = int(volume['volume'])
                except Exception as e:
                    print(f'volume number is not a interger, skipping')
                    continue
                create_volume(volume, po, language)


def create_volume(volume, po, language):
    if 'image_url' in volume and volume['image_url']:
        image = volume['image_url']
    else:
        image = 'https://i.ibb.co/82Fb1DC/47b000fb-c5af-451a-a6b2-580e7b4c81bc-copy.png'
    output_dir = 'covers'
    create_output_directory(output_dir)
    with requests.Session() as session:
        sucess, _ = download_image(session, image, output_dir, f"{po.name} - {volume['volume']}")
        # print(sucess)
    # print(f'{po.name} - {volume["volume"]}')
    image_path = find_cover_path(f'{po.name} - {volume["volume"]}')
    # print(image_path)
    with Image.open(image_path) as img:
        image_io = BytesIO()
        img.save(image_io, format=img.format)
        image_io.seek(0)
        img = File(image_io, name=f'{po.name} - {volume["volume"]}.jpg')
    # print(language)
    Volume.objects.create(
        product=po,
        volume_number=volume['volume'],
        price=8000,
        image=img,
        start_chapter=volume['start_chapter'],
        end_chapter=volume['end_chapter'],
        language=language
    )
    os.remove(image_path)
