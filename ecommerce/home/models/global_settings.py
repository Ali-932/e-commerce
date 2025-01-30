from django.db import models
from djmoney.models.fields import MoneyField

from ecommerce.home.models.singleton import SingletonModel


class Global(SingletonModel):
    delivery_price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=5000)
    delivery_price_outside_baghdad = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=6000)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)