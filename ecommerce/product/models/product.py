from django.contrib.postgres.fields import ArrayField
from django.db import models

from ecommerce.abstract.utlites.menu_nums import DemographicChoices, ThemeChoices, GenresChoices


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
    title_arabic = models.CharField(max_length=200, null=True, blank=True)
    title_synonyms = ArrayField(
        models.CharField(max_length=100, null=True, blank=True),
        default=list,
    )

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


# class Item(models.Model):
#     name = models.CharField(max_length=400)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_available = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
