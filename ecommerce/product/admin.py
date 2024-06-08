from django import forms
from django.contrib import admin
from .models import Product, Volume, ProductBanner, SpecialOfferProducts
from ..abstract.utlites.menu_nums import CategoryChoices




class SpecialOfferProductsAdmin(admin.ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ["language", "quantity", "price", "volume"]
    search_fields = ["language"]
    list_filter = ["language"]

admin.site.register(SpecialOfferProducts, SpecialOfferProductsAdmin)
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
