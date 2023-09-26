from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div
from django import forms
from django.urls import reverse_lazy

from ecommerce.order.models import OrderItem


class ProductForm(forms.Form):
    quantity = forms.CharField(label='الكمية', required=True,widget=forms.TextInput(
        attrs={'class': 'form-control qty','type':'number', 'id':'qty',
               'value':'1', 'min':'1', 'max':'10', 'step':'1', 'data-decimals':'0'}))
    language = forms.CharField(label='اللغة', required=True, widget=forms.Select(attrs={'class': 'form-control'}, choices=OrderItem.Language_CHOICES.choices))

    # def __init__(self, *args, **kwargs):
    #
    #     self.form_action = kwargs.pop('form_action', None)
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.form_action = self.form_action or reverse_lazy('orders:set_order')
    #     self.helper.layout = Layout(
    #             Column(
    #                 Row(
    #                 Div(
    #                 'quantity',
    #                 css_class='product-details-quantity mr-2'
    #                 ),
    #                 ),
    #                 Row(
    #                 'language',
    #                 )
    #             ),
    #
    #         Submit('submit', 'حفظ', css_class='btn btn-primary')
    #     )

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     parent = cleaned_data['tn_parent']
    #     code = cleaned_data['code']
    #
    #     if not self.form_action and Account.objects.filter(tn_parent=parent, code=code).exists():
    #         raise forms.ValidationError('لا يمكن تكرار نفس الحساب بنفس الترميز لنفس التبويب.')
