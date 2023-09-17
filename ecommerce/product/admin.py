from django import forms
from django.contrib import admin
from .models import Product, Volume, ProductBanner
from ..abstract.utlites.menu_nums import CategoryChoices




# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ["name", "born_location", "born_date"]
#     search_fields = ["name"]
#
# admin.site.register(Author, AuthorAdmin)
#

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
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')

admin.site.register(ProductBanner, AAdmin)
