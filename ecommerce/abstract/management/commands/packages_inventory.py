from django.core.management.base import BaseCommand
from django.core.management import call_command
from ecommerce.product.models import *
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        VolumesPackage.objects.filter(Q(package_name="باكج فوجا بوند") | Q(package_name="باكج جنة الجحيم")).delete()
        vp1, created = VolumesPackage.objects.get_or_create(
            package_name="باكج فوجا بوند",
            start_volume=17,
            end_volume=22,
            price=Money(50000, 'IQD'),
            volume_count=6,
            image='images/packages/vaga.jpg',
            product_id=809
        )
        volumes = Volume.objects.filter(id__in=[4836, 4837, 4838, 4839, 4840, 4841])
        vp1.volumes.add(*volumes)
        vp2, created = VolumesPackage.objects.get_or_create(
            package_name="باكج جنة الجحيم",
            start_volume=5,
            end_volume=12,
            price=Money(60000, 'IQD'),
            volume_count=8,
            image='images/packages/hell.jpg',
            product_id=1365
        )
        volumes = Volume.objects.filter(id__in=[8219, 8220, 8221, 8222, 8223, 8224, 8225, 8226])
        vp2.volumes.add(*volumes)

        ### Inventory Products

        InventoryProduct.objects.get_or_create(
            volume_id=8219,
            language='AR',
            quantity=1,
            is_available=True
        )

        InventoryProduct.objects.get_or_create(
            volume_id=8220,
            language='AR',
            quantity=1,
            is_available=True
        )
