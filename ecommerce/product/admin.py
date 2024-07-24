from django import forms
from django.contrib import admin
from django.db import transaction

from .models import Product, Volume, ProductBanner, VolumesPackage, InventoryProduct
from ..abstract.utlites.menu_nums import CategoryChoices
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



class InventoryProductForm(forms.ModelForm):
    class Meta:
        model = InventoryProduct
        fields = 'language', 'quantity', 'price', 'volume'

class InventoryProductAdmin(admin.ModelAdmin):
    form = InventoryProductForm
    raw_id_fields = ('volume',)
    list_display = ["language", "quantity", "price", "volume"]
    search_fields = ["language"]
    list_filter = ["language"]

admin.site.register(InventoryProduct, InventoryProductAdmin)









class VolumePackageForm(forms.ModelForm):
    # volumes = forms.MultipleChoiceField(choices=Volume.objects.all())
    image_upload = forms.ImageField(required=False)  # Change FileField to ImageField if you're dealing with images
    class Meta:
        model = VolumesPackage
        fields = 'price', 'volumes', 'image_upload'
        widgets = {
            'image_upload': forms.FileInput(attrs={'accept': 'image/*'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        print("Form data:", self.data)
        print("Files:", self.files)
        print("Cleaned data:", cleaned_data)
        return cleaned_data



class VolumesPackageAdmin(admin.ModelAdmin):
    form = VolumePackageForm
    raw_id_fields = ('volumes',)
    list_display = ["product", "price", "created_at"]
    search_fields = ["product__name"]
    list_filter = ["product"]

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        print("Request POST:", request.POST)
        print("Request FILES:", request.FILES)

        if form.is_valid():
            # Handle image upload
            if image := form.cleaned_data.get('image_upload'):
                path = default_storage.save(f'volumes_package/{image.name}', ContentFile(image.read()))
                obj.image = default_storage.url(path)

            # Set type to 'Package'
            obj.type = 'Package'

            # # Save the object if it's new
            # if not obj.id:
            #     super().save_model(request, obj, form, change)

            print('here')
            # Now we can access the many-to-many relationship
            if form.cleaned_data.get('volumes'):
                volumes = Volume.objects.filter(id__in=form.cleaned_data.get('volumes'))
                print('exist')
                print(obj.volumes.values_list('product', flat=True).distinct())
                if volumes.values_list('product', flat=True).distinct().count() > 1:
                    raise ValueError('All volumes must belong to the same product')

                obj.product = volumes.first().product
                obj.start_volume = volumes.order_by('volume_number').first().volume_number
                obj.end_volume = volumes.order_by('-volume_number').first().volume_number
                obj.volume_count = volumes.count()

            # Save again to update the fields we just set
            super().save_model(request, obj, form, change)
        else:
            print("Form errors:", form.errors)

admin.site.register(VolumesPackage, VolumesPackageAdmin)












class ProductForm(forms.ModelForm):
    category = forms.MultipleChoiceField(choices=CategoryChoices.choices)

    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]
    form = ProductForm
admin.site.register(Product, ProductAdmin)


class VolumeAdmin(admin.ModelAdmin):
    list_display = ["product", "volume_number", "price", "created_at"]
    search_fields = ["product__name"]
    list_filter = ["product"]

admin.site.register(Volume, VolumeAdmin)

class AAdmin(admin.ModelAdmin):
    # Customize the admin options for your model
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image','active')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')

admin.site.register(ProductBanner, AAdmin)
