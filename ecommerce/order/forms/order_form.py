from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div, HTML
from django import forms
from django.core.validators import RegexValidator
from django.urls import reverse_lazy

from ecommerce.abstract.models.choices import ProvinceChoices
from ecommerce.order.models import ShippingAddress


class OrderForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude =  ('order','user',)

    starts_with_07 = RegexValidator(r'^07', 'Field must start with "07".')
    digits_only = RegexValidator(r'^\d{11}$', 'Field must be exactly 11 digits.')

    name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}), label="الاسم")
    province = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ProvinceChoices.choices,label="المحافظة")
    address=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}),label="العنوان")
    phone=forms.CharField(max_length=11,widget=forms.TextInput(attrs={'class':'form-control'}),validators=[digits_only,starts_with_07],label="رقم الهاتف الاول")
    phone2=forms.CharField(max_length=11,widget=forms.TextInput(attrs={'class':'form-control'}),validators=[digits_only,starts_with_07],required=False,label="رقم الهاتف الثاني")
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'}),required=False,label="البريد الالكتروني")
    notes=forms.CharField(max_length=400,widget=forms.Textarea(attrs={'class':'form-control'}),required=False,label="ملاحظات")
    instagram_user=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}),required=False,label="اسم المستخدم في الانستغرام")
    defualt_address=forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-check-input'}),required=False,label="هل تريد اني يكون هذا عنوانك الافتراضي؟")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            HTML("""
                    <p class ='arabic-font force-rtl mr-1 mb-1'>الحقول التي تحتوي على علامة النجمة *  <strong>الزامية </strong> اما الباقي تعتبر اختيارية</p>
                """),
        Column(
            Row(
                    'name',
                    'instagram_user', css_class='col-10 justify-content-around'


                ),
            Row(
                    'province',
                    'address', css_class='col-8 justify-content-around'
            )

        ),
            Row(
                    'phone',
                    'phone2', css_class='col-10 justify-content-around'
            ),
                    'email',
            Row(
                'defualt_address', template='abstract/widgets/rtl_checkbox.html')
            ,
            'notes',
            )

