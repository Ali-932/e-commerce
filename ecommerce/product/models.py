from django.contrib.postgres.fields import ArrayField
from django.db import models
from djmoney.models.fields import MoneyField

from ecommerce.abstract.utlites.menu_nums import CategoryChoices


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='authors', null=True, blank=True)
    born_location = models.CharField(max_length=100, null=True, blank=True)
    born_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = ArrayField(
        models.CharField(max_length=100, choices=CategoryChoices.choices,default=CategoryChoices.SHONEN),
    )
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class Volume(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    volume_number = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='IQD', default=8000)
    image = models.ImageField(upload_to='volumes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_chapter = models.IntegerField(null=True, blank=True)
    end_chapter = models.IntegerField(null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Volumes'

    def __str__(self):
        return f'{self.product.name} {self.volume_number}'
