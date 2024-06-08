from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from ecommerce.account.models import User
from ecommerce.order.models import ShippingAddress


@receiver(post_save, sender=User)
def create_address(sender, instance,created, **kwargs):
    if created and not instance.is_superuser:
        ShippingAddress.objects.create(user=instance,
                                   name=instance.name,
                                   province=instance.province,
                                   address=instance.address1,
                                   phone=instance.phone_number_1,
                                   phone2=instance.phone_number_2,
                                   email=instance.email,
                                   is_active=True
                                   )
