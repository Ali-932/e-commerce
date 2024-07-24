from django.db import models

from ecommerce.home.models import AdModel


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
