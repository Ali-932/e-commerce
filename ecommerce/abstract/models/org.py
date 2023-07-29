from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

class AdImages(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.image.name