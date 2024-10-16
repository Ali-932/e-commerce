from django.db import models


# Create your models here.
class ADTypeChoices(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'
    C = 'C', 'C'
    D = 'D', 'D'
    VA = 'VA', 'VA'
    VB = 'VB', 'VB'


class AdModel(models.Model):
    Title = models.CharField(max_length=100, blank=True, null=True)
    Description = models.TextField()
    image = models.ImageField(upload_to='images/ad/')
    type = models.CharField(max_length=2, choices=ADTypeChoices.choices, default=ADTypeChoices.A, editable=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    active = models.BooleanField(default=False)
    prompt_text = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    volume = models.OneToOneField('product.Volume', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'
        unique_together = ['type', 'active']


class AModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='A')


class AModel(AdModel):
    objects = AModelManger()

    class Meta:
        proxy = True
        verbose_name = 'bigger ad'

    def save(self, *args, **kwargs):
        self.type = 'A'
        super().save(*args, **kwargs)


class BModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='B')


class BModel(AdModel):
    objects = BModelManger()

    class Meta:
        proxy = True
        verbose_name = 'middle ad'

    def save(self, *args, **kwargs):
        self.type = 'B'
        super().save(*args, **kwargs)


class CModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='C')


class CModel(AdModel):
    objects = CModelManger()

    class Meta:
        proxy = True
        verbose_name = 'Small Ad 1'

    def save(self, *args, **kwargs):
        self.type = 'C'
        super().save(*args, **kwargs)


class DModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='D')


class DModel(AdModel):
    objects = DModelManger()

    class Meta:
        proxy = True
        verbose_name = 'Small Ad 2'

    def save(self, *args, **kwargs):
        self.type = 'D'
        super().save(*args, **kwargs)




class VolumeAModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='VA')


class VolumeABanner(AdModel):
    objects = VolumeAModelManger()

    class Meta:
        proxy = True
        verbose_name = 'Volume A Banner'

    def save(self, *args, **kwargs):
        self.type = 'VA'
        super().save(*args, **kwargs)



class VolumeBModelManger(models.Manager):
    def get_queryset(self):
        # Custom logic for querying the model
        return super().get_queryset().filter(type='VB')


class VolumeBBanner(AdModel):
    objects = VolumeBModelManger()

    class Meta:
        proxy = True
        verbose_name = 'Volume B Banner'

    def save(self, *args, **kwargs):
        self.type = 'VB'
        super().save(*args, **kwargs)


