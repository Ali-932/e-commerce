from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.urls import reverse

from ecommerce.home.models import *
from ecommerce.product.models import VolumesPackage


class Command(BaseCommand):
    def handle(self, *args, **options):
        AdModel.objects.all().delete()
        call_command('packages_inventory')
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
            link=reverse('home:quality_rep'),
            prompt_text='جودة العمل'
        )

        package_pk = VolumesPackage.objects.get(package_name="باكج جنة الجحيم").pk
        CModel.objects.get_or_create(
            Title='باكج جديد!',
            Description='باكج جحيم الجنة الجديد',
            image='images/ad/banner-3_copy_AuITbPl.jpg',
            type=ADTypeChoices.C,
            active=True,
            link=reverse('product:view-product', kwargs={'pk': package_pk}),
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

        VolumeABanner.objects.get_or_create(
            Title='قصة رعب جديد!',
            image='images/ad/ito banner copy.jpg',
            volume_id=4812,
            active=True,
        )

        VolumeBBanner.objects.get_or_create(
            Title='جوجوتسو بمجلد اخير!',
            image='images/ad/photo_2023-10-01_18-59-56REÀí_tezCbXL.png',
            volume_id=88,
            active=True,

        )

    # call_command('upload_manga')
