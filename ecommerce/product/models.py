from django.contrib.postgres.fields import ArrayField
from django.db import models
from djmoney.models.fields import MoneyField

from ecommerce.abstract.utlites.menu_nums import CategoryChoices,DemographicChoices,ThemeChoices,GenresChoices

# class Author(models.Model):
#     name = models.CharField(max_length=100)
#     bio = models.TextField(null=True, blank=True)
#     image = models.ImageField(upload_to='authors', null=True, blank=True)
#     born_location = models.CharField(max_length=100, null=True, blank=True)
#     born_date = models.DateField(null=True, blank=True)
#     role = models.CharField(max_length=100, null=True, blank=True)
#     class Meta:
#         verbose_name_plural = 'Authors'
#         indexes = [
#             models.Index(fields=['name', 'role']),
#         ]
#
#     def __str__(self):
#         return self.name
#

class Product(models.Model):
    class ProductType(models.TextChoices):
        Manga = 'مانجا', 'Manga'
        Light_Novel = 'رواية خفيفة', 'Light Novel'
        Manhwa = 'مانهوا', 'Manhwa'
        Comic = 'كوميك', 'Comic'

    name = models.CharField(max_length=400)
    genres = ArrayField(
        models.CharField(max_length=100, choices=GenresChoices.choices,null=True, blank=True),
        default=list,
    )
    themes = ArrayField(
        models.CharField(max_length=100, choices=ThemeChoices.choices,null=True, blank=True),
        default=list,
    )
    demographics = ArrayField(
        models.CharField(max_length=100, choices=DemographicChoices.choices,null=True, blank=True),
        default=list,
    )
    synopsis = models.TextField(null=True, blank=True)
    background = models.TextField(null=True, blank=True)
    author = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, null=True, blank=True, choices=ProductType.choices)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    volumes = models.IntegerField(null=True, blank=True)
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


class Volume(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    volume_number = models.IntegerField(null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    image = models.URLField(max_length=300,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_chapter = models.IntegerField(null=True, blank=True)
    end_chapter = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Volumes'

    def __str__(self):
        return f'{self.product.name} {self.volume_number}'
