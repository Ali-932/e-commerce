import ast
import json

from django.core.management.base import BaseCommand
from django.db.models import Count

from ecommerce.product.models import Product, Volume
import json

class Command(BaseCommand):
    help = "upload accounts (create COA)"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('ecommerce/product/management/commands/fixtures/Anime1Gmanga3.json','r',encoding='utf-8') as f:
            jsonf= json.load(f)
        self.handel_authers(jsonf)

    def handel_authers(self, jsonf):
        Product.objects.all().delete()
        Volume.objects.all().delete()

        for i in jsonf:
            str_list= i['manga']['authors']
            str_list = str_list.replace("'", '"')
            list_obj = json.loads(str_list)
            au={}
            for author in list_obj:
                first=author['first_name']
                last=author['last_name']
                au[f'{first} {last}']=author['role']
            self.handel_product(i,au)


    def handel_product(self,i,au):
        genres, demo, title_synonyms, themes = map(
            ast.literal_eval, (i['manga']['genres'],
            i['manga']['demographics'],
           i['manga']['title_synonyms'], i['manga']['themes']))
        print(type(au))
        po=Product.objects.create(
            name=i['manga']['title'],
            type='Manga',
            genres=genres,
            themes=themes,
            demographics=demo,
            synopsis=i['manga']['synopsis'],
            background=i['manga']['background'],
            start_date=i['manga']['start_date'],
            end_date=i['manga']['end_date'],
            score=i['manga']['score'],
            favorites=i['manga']['favorites'],
            title_japanese=i['manga']['title_japanese'],
            title_english=i['manga']['title_english'],
            title_synonyms=title_synonyms,
            author=au
        )
        # print(po.objects.values('author'))
        self.handel_volumes(po, i)

    def handel_volumes(self, po, i):
        for volume in i['manga']['volumes']:
            if 'image_url' in volume:
                image=volume['image_url']
            else:
                image='https://i.ibb.co/82Fb1DC/47b000fb-c5af-451a-a6b2-580e7b4c81bc-copy.png'
                print('in else')
            Volume.objects.create(
                product=po,
                volume_number=volume['volume'],
                price=8000,
                image=image,
                start_chapter=volume['start_chapter'],
                end_chapter=volume['end_chapter'],
            )
