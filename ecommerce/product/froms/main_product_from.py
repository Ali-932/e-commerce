from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div
from django import forms
from django.urls import reverse_lazy

from ecommerce.order.models import OrderItem


class ProductForm(forms.Form):
    quantity = forms.CharField(label='الكمية', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control qty', 'type': 'number', 'id': 'qty',
               'value': '1', 'min': '1', 'max': '10', 'step': '1', 'data-decimals': '0'}))
    language = forms.CharField(label='اللغة', required=True,
                               widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_language',
                                                          'name': 'language'},
                                                   choices=OrderItem.Language_CHOICES.choices))
    price = forms.DecimalField(label='السعر', required=True, decimal_places=5, widget=forms.NumberInput(
        attrs={'class': 'form control', 'name': 'price', 'id': 'price_id'}
    ))

