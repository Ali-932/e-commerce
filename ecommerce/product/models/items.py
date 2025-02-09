import os
from io import BytesIO

from PIL import Image
from django.db import models, transaction
from djmoney.models.fields import MoneyField

from ecommerce.product.models import Product
from djmoney.money import Money
from django.core.files import File

class VolumesPackageMixins(models.Model):
    # product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='package')
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=-1)
    volumes = models.ManyToManyField('Volume', related_name='package', symmetrical=False)
    start_volume = models.IntegerField(null=True, blank=True)
    end_volume = models.IntegerField(null=True, blank=True)
    volume_count = models.IntegerField(null=True, blank=True)
    package_name = models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        abstract = True


class VolumeMixins(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='volume')
    volume_number = models.IntegerField(null=True, blank=True)
    # price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    # image = models.URLField(max_length=300, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    start_chapter = models.IntegerField(null=True, blank=True)
    end_chapter = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class InventoryProductMixins(models.Model):
    class Language_CHOICES(models.TextChoices):
        AR = 'AR', 'عربي'
        EN = 'EN', 'انكليزي'
        BOTH = 'BOTH', 'عربي وانكليزي' # this is not related to inventory products

    language = models.CharField(max_length=4, choices=Language_CHOICES.choices, default=Language_CHOICES.AR)
    quantity = models.IntegerField(default=0)
    # price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=5000)
    # created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=False, editable=False)
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE, related_name='inventory_product', null=True, blank=True)

    class Meta:
        abstract = True


class Item(VolumesPackageMixins, VolumeMixins, InventoryProductMixins):
    class Type_CHOICES(models.TextChoices):
        Volume = 'Volume', 'Volume'
        Package = 'Package', 'Package'
        InventoryProduct = 'Inventory_Manga', 'Inventory_Manga'

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='volume')
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    image = models.ImageField(max_length=300, null=True, blank=True, upload_to='images/covers/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=50, default='Volume', choices=Type_CHOICES.choices)


    def make_thumbnail(self):
        image = Image.open(self.image)
        image = image.convert('RGB')

        # Define the size
        size = (300, 300)

        image.thumbnail(size, Image.LANCZOS)

        thumb_io = BytesIO()
        image.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=os.path.basename(self.image.name))
        self.thumbnail.save(thumbnail.name, thumbnail, save=False)
        return True

    def __str__(self):
        if self.type == 'Package':
            return f'{self.product.name} - {self.package_name}'
        return f'{self.product.name} - {self.volume_number}'

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail')
        super(Item, self).save(*args, **kwargs)

class VolumeManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Volume')


class Volume(Item):
    class Meta:
        proxy = True
        verbose_name = 'Volume'
        verbose_name_plural = 'Volumes'

    objects = VolumeManger()

    def __str__(self):
        return f'{self.product.name} - {self.volume_number}'

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail')
        super(Volume, self).save(*args, **kwargs)


class VolumesPackageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Package')


class VolumesPackage(Item):
    class Meta:
        proxy = True
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    objects = VolumesPackageManager()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.type = 'Package'
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail')
        super().save(force_insert, force_update, using, update_fields)


class InventoryProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Inventory_Manga')


class InventoryProduct(Item):
    class Meta:
        proxy = True
        verbose_name = 'Inventory Manga'
        verbose_name_plural = 'Inventory Mangas'

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.is_available = self.quantity > 0
        self.type = 'Inventory_Manga'
        self.product = self.volume.product
        self.image = self.volume.image
        self.volume_number = self.volume.volume_number
        self.start_chapter = self.volume.start_chapter
        self.end_chapter = self.volume.end_chapter
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail')

        super().save(*args, **kwargs)


    objects = InventoryProductManager()
