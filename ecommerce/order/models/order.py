from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from djmoney.models.fields import MoneyField
from shortuuid.django_fields import ShortUUIDField

from ecommerce.abstract.models.choices import ProvinceChoices
from ecommerce.account.models import User
from ecommerce.product.models import Volume


class Order(models.Model):
    class Status_CHOICES(models.TextChoices):
        PENDING = 'قيد الانتظار', 'pending'
        CONFIRMED = 'تم التأكيد من قبل الزبون', 'confirmed'
        ON_WORK = 'قيد العمل', 'on_work'
        CANCELED = 'ملغي', 'canceled'
        DELIVERED = 'تم التوصيل', 'delivered'
        RETURNED = 'راجع', 'returned'

    class Payment_CHOICES(models.TextChoices):
        CASH = 'كاش', 'cash'
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    total_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=Status_CHOICES.choices, default=Status_CHOICES.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=100, choices=Payment_CHOICES.choices, default=Payment_CHOICES.CASH)
    notes = models.TextField(blank=True, null=True)
    discount = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    uuid = ShortUUIDField(length=8, max_length=8)

class OrderItem(models.Model):
    class Language_CHOICES(models.TextChoices):
        AR = 'AR', 'عربي'
        EN = 'EN', 'انكليزي'
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True, blank=True) #it should be forginkey to have multuple same volume in different lagnuges
    quantity = models.IntegerField(default=0)
    single_piece_price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    price = MoneyField(max_digits=14, decimal_places=0, default_currency='IQD', default=8000)
    language = models.CharField(max_length=100, choices=Language_CHOICES.choices, default=Language_CHOICES.AR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(default=0)

    class meta:
        unique_together = ('order', 'volume', 'language')

@receiver(pre_save, sender=OrderItem)
def calculate_price(sender, instance, **kwargs):
    if instance.quantity!=0:
        instance.single_piece_price.amount = instance.price.amount
        instance.price.amount*=Decimal(instance.quantity)

class ShippingAddress(models.Model):
    name=models.CharField(max_length=100)
    province= models.CharField(max_length=100,choices=ProvinceChoices.choices)
    address=models.TextField()
    phone=models.CharField(max_length=100)
    phone2=models.CharField(max_length=100,blank=True,null=True)
    order=models.OneToOneField(Order,on_delete=models.CASCADE,null=True,blank=True)
    email=models.EmailField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    instagram_username = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)


