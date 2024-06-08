from django.db import models
from djmoney.models.fields import MoneyField

from ecommerce.home.models.singleton import SingletonModel


class Global(SingletonModel):
    delivery_price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=5000)