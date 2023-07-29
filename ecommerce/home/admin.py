from django.contrib import admin

# Register your models here.

from .models import AModel, BModel, CModel, DModel
from .models import nav_ad

class AAdmin(admin.ModelAdmin):
    # Customize the admin options for your model
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')


admin.site.register(AModel, AAdmin)


class BAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')


admin.site.register(BModel, BAdmin)


class CAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')


admin.site.register(CModel, CAdmin)

class DAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'image')
    list_filter = ('Title', 'Description')
    search_fields = ('Title', 'Description')

admin.site.register(DModel, DAdmin)


class NAVAdmin(admin.ModelAdmin):
    list_display = ('char', 'icon', 'active')
    list_filter = ('char', 'active')
    search_fields = ('char', 'active')

admin.site.register(nav_ad, NAVAdmin)
