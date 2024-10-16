from django import forms
from django.contrib import admin

# Register your models here.

from .models import AModel, BModel, CModel, DModel, Global, VolumeABanner, VolumeBBanner
from .models import nav_ad
admin.site.site_header = 'Manga Store Admin'
class AAdmin(admin.ModelAdmin):
    # Customize the admin options for your model
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')


admin.site.register(AModel, AAdmin)


class BAdmin(admin.ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')


admin.site.register(BModel, BAdmin)


class CAdmin(admin.ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')


admin.site.register(CModel, CAdmin)

class DAdmin(admin.ModelAdmin):
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')

admin.site.register(DModel, DAdmin)


class NAVAdmin(admin.ModelAdmin):
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

class VolumeAAdmin(admin.ModelAdmin):
    form = VolumeAForm
    raw_id_fields = ('volume',)
    list_display = ('Title', 'Description', 'image','active')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')
admin.site.register(VolumeABanner, VolumeAAdmin)
admin.site.register(VolumeBBanner, VolumeAAdmin)
