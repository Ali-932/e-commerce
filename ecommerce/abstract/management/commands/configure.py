from django.core.management.base import BaseCommand
from django.core.management import call_command
from ecommerce.home.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        AdModel.objects.all().delete()

        nav_ad.objects.get_or_create(char='تمتع  بلقرائة مع القهوة', icon='bi bi-cup-hot', active=True)

        AModel.objects.get_or_create(
            Title='بمناسبة افتتاح متجرنا الإلكتروني',
            Description='تخفيض 20 % عند شراء اي منتج من الموقع',
            image='images/ad/Untitled_design.png',
            active=True,
            type=ADTypeChoices.A)
        BModel.objects.get_or_create(
            Title='ليش مانجا ستور؟',
            Description='خبرة اكثر من 7 سنين في مجال المانجات',
            image='images/ad/1056_copy_3.jpg',
            type=ADTypeChoices.B,
            active=True,
            link=None,
            prompt_text='جودة العمل'
        )
        CModel.objects.get_or_create(
            Title='باكج جديد!',
            Description='باكج جحيم الجنة الجديد',
            image='images/ad/banner-3_copy_AuITbPl.jpg',
            type=ADTypeChoices.C,
            active=True,
            link=None,
            prompt_text='اعرض الباكج'
        )

        DModel.objects.get_or_create(
            Title='@manga_store1',
            Description='اطلب اي عنوان من صفحة الانستغرام الخاصة بنا',
            image='images/ad/44.jpg',
            type=ADTypeChoices.D,
            active=True,
            link=None,
            prompt_text=None
        )

    # call_command('upload_manga')