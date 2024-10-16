from django.db import models


class nav_ad(models.Model):
    char = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False, unique=True)
    datetime = models.DateTimeField(auto_now_add=True)
