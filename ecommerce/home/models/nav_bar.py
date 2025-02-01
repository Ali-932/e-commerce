from django.db import models
from django.db.models import Q


class nav_ad(models.Model):
    char = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.active:
            nav_ad.objects.filter(~Q(pk=self.pk)).update(active=False)
        super(nav_ad, self).save(force_insert, force_update, using, update_fields)
