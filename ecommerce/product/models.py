from django.contrib.postgres.fields import ArrayField
from django.db import models
from djmoney.models.fields import MoneyField

from ecommerce.abstract.utlites.menu_nums import DemographicChoices, ThemeChoices, GenresChoices
from ecommerce.home.models import AdModel


class Product(models.Model):
    class ProductType(models.TextChoices):
        Manga = 'مانجا', 'Manga'
        Light_Novel = 'رواية خفيفة', 'Light Novel'
        Manhwa = 'مانهوا', 'Manhwa'
        Comic = 'كوميك', 'Comic'

    name = models.CharField(max_length=400)
    genres = ArrayField(
        models.CharField(max_length=100, choices=GenresChoices.choices, null=True, blank=True),
        default=list,
    )
    themes = ArrayField(
        models.CharField(max_length=100, choices=ThemeChoices.choices, null=True, blank=True),
        default=list,
    )
    demographics = ArrayField(
        models.CharField(max_length=100, choices=DemographicChoices.choices, null=True, blank=True),
        default=list,
    )
    synopsis = models.TextField(null=True, blank=True)
    background = models.TextField(null=True, blank=True)
    author = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, null=True, blank=True, choices=ProductType.choices)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    favorites = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    title_japanese = models.CharField(max_length=200, null=True, blank=True)
    title_english = models.CharField(max_length=200, null=True, blank=True)
    title_synonyms = ArrayField(
        models.CharField(max_length=100, null=True, blank=True),
        default=list,
    )

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

class VolumesPackage(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT, related_name='package')
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=-1)
    image = models.ImageField(upload_to='images/packages', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    volumes = models.ManyToManyField('Volume', related_name='package')

class Volume(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='volume')
    volume_number = models.IntegerField(null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    image = models.URLField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_chapter = models.IntegerField(null=True, blank=True)
    end_chapter = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Volumes'

    def __str__(self):
        return f'{self.product.name} {self.volume_number}'

class SpecialOfferProducts(models.Model):
    class Language_CHOICES(models.TextChoices):
        AR = 'AR', 'عربي'
        EN = 'EN', 'انكليزي'

    language = models.CharField(max_length=2, choices=Language_CHOICES.choices, default=Language_CHOICES.AR)
    quantity = models.IntegerField(default=0)
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=False, editable=False)
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE, related_name='special_offer', null=True, blank=True)

    class Meta:
        unique_together = ('language', 'volume')

    def save(self, *args, **kwargs):
        self.is_available = self.quantity > 0
        super().save(*args, **kwargs)


class PModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='P')


class ProductBanner(AdModel):
    objects = PModelManger()

    class Meta:
        proxy = True
        verbose_name = 'product banner'

    def save(self, *args, **kwargs):
        self.type = 'P'
        super().save(*args, **kwargs)
