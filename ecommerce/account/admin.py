from django.contrib import admin

# Register your models here.

from ecommerce.account.models import User

admin.site.register(User)