from django import forms
from django.contrib import admin
from .models import Author, Product, Volume
from ..abstract.utlites.menu_nums import CategoryChoices




class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "born_location", "born_date"]
    search_fields = ["name"]

admin.site.register(Author, AuthorAdmin)


class ProductForm(forms.ModelForm):
    category = forms.MultipleChoiceField(choices=CategoryChoices.choices)

    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "author", "created_at"]
    search_fields = ["name"]
    list_filter = ["category", "author"]
    form = ProductForm
admin.site.register(Product, ProductAdmin)


class VolumeAdmin(admin.ModelAdmin):
    list_display = ["product", "volume_number", "price", "created_at"]
    search_fields = ["product__name"]
    list_filter = ["product"]

admin.site.register(Volume, VolumeAdmin)
