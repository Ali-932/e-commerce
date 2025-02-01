# admin.py
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline, StackedInline

from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0  # Number of extra blank forms
    readonly_fields = ('created_at', 'updated_at')
    fields = (
        'item',
        'quantity',
        'single_piece_price',
        'price',
        'language',
        'discount',
    )
    autocomplete_fields = ('item',)

class ShippingAddressInline(StackedInline):
    model = ShippingAddress
    extra = 0
    max_num = 1  # Only one shipping address per order
    readonly_fields = ('created_at', 'updated_at')
    fields = (
        'name',
        'province',
        'address',
        'phone',
        'phone2',
        'email',
        'instagram_username',
        'is_active',
    )


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """Unfold-based admin for managing orders along with their items and shipping address."""
    inlines = [OrderItemInline, ShippingAddressInline]

    list_display = (
        'uuid',
        'user',
        'status',
        'total_price',
        'total_quantity',
        'active',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status',
        'active',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'uuid',
        'user__username',
        'user__name',
    )
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': (
                'user',
                'uuid',
                'status',
                'payment_method',
                'total_price',
                'total_quantity',
                'discount',
                'notes',
                'active',
            )
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )


