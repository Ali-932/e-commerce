from django.core.management.base import BaseCommand
from django.core.management import call_command
from ecommerce.product.models import *
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        VolumesPackage.objects.filter(Q(package_name="باكج فوجا بوند") | Q(package_name="باكج جنة الجحيم")).delete()

        vagabond_product = Product.objects.get(name = 'Vagabond').pk
        vp1, created = VolumesPackage.objects.get_or_create(
            package_name="باكج فوجا بوند",
            start_volume=17,
            end_volume=22,
            price=Money(50000, 'IQD'),
            volume_count=6,
            image='images/packages/vaga.jpg',
            product_id=vagabond_product
        )
        volumes = Volume.objects.filter(product_id=vagabond_product, volume_id__gte=17, volume_id__lte=22)
        # volumes = Volume.objects.filter(id__in=[4836, 4837, 4838, 4839, 4840, 4841])
        vp1.volumes.add(*volumes)

        jigokuraku_product = Product.objects.get(name = 'Jigokuraku').pk
        vp2, created = VolumesPackage.objects.get_or_create(
            package_name="باكج جنة الجحيم",
            start_volume=5,
            end_volume=12,
            price=Money(60000, 'IQD'),
            volume_count=8,
            image='images/packages/hell.jpg',
            product_id=jigokuraku_product
        )
        volumes = Volume.objects.filter(product_id=jigokuraku_product, volume_id__gte=5, volume_id__lte=12)
        # volumes = Volume.objects.filter(id__in=[8219, 8220, 8221, 8222, 8223, 8224, 8225, 8226])
        vp2.volumes.add(*volumes)

        ### Inventory Products
        random_volume1 = Volume.objects.order_by('?').first().pk
        random_volume2 = Volume.objects.order_by('?').first().pk
        InventoryProduct.objects.create(
            volume_id=random_volume1,
            language='AR',
            quantity=1,
            is_available=True
        )

        InventoryProduct.objects.create(
            volume_id=random_volume2,
            language='AR',
            quantity=1,
            is_available=True
        )
