from django import forms
from django.contrib import admin

# Register your models here.

from .models import AModel, BModel, CModel, DModel, Global, VolumeABanner, VolumeBBanner
from .models import nav_ad
from unfold.admin import ModelAdmin
admin.site.site_header = 'Manga Store Admin'
class AAdmin(ModelAdmin):
    # Customize the admin options for your model
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')
    autocomplete_fields = ['volume']



admin.site.register(AModel, AAdmin)


class BAdmin(ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')
    autocomplete_fields = ['volume']


admin.site.register(BModel, BAdmin)


class CAdmin(ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')
    autocomplete_fields = ['volume']


admin.site.register(CModel, CAdmin)

class DAdmin(ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')
    autocomplete_fields = ['volume']

admin.site.register(DModel, DAdmin)


class NAVAdmin(ModelAdmin):
    list_display = ('char', 'icon', 'active')
    list_filter = ('char', 'active')
    search_fields = ('char', 'active')

admin.site.register(nav_ad, NAVAdmin)


# admin.site.register(Global)





class VolumeAForm(forms.ModelForm):
    class Meta:
        model = VolumeABanner
        fields = (
            'Title',
            'Description',
            'image',
            'prompt_text',
            'link',
            'volume',
            'active'
        )

class VolumeAAdmin(ModelAdmin):
    form = VolumeAForm
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image','active')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')
    autocomplete_fields = ['volume']

admin.site.register(VolumeABanner, VolumeAAdmin)
admin.site.register(VolumeBBanner, VolumeAAdmin)


class GlobalAdmin(admin.ModelAdmin):
    list_display = ["delivery_price", "delivery_price_outside_baghdad", "discount"]


admin.site.register(Global, GlobalAdmin)
