from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Field, Div, HTML
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.urls import reverse_lazy
from ecommerce.abstract.models.choices import ProvinceChoices
from ecommerce.account.models import User
from crispy_forms.bootstrap import FieldWithButtons, StrictButton


class DateInput(forms.DateInput):
    input_type = 'date'


class RegisterForm(forms.ModelForm):
    english_username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]+$',
        message="اسم المستخدم يجب أن يكون بالأحرف الإنجليزية والأرقام فقط."
    )

    class Meta:
        model = User
        fields = '__all__'
        exclude = ['is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'last_login', 'date_joined']

    starts_with_07 = RegexValidator(r'^07', 'يجب أن يبدأ الحقل بـ 07.')
    digits_only = RegexValidator(r'^\d{11}$', 'يجب أن يحتوي رقم الهاتف على 11 رقم.')

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label="الاسم")
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label="اسم المستخدم", validators=[english_username_validator])
    province = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=ProvinceChoices.choices,
                                 label="المحافظة")
    address1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label="العنوان")
    phone_number_1 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     validators=[digits_only, starts_with_07], label="رقم الهاتف الاول")
    phone_number_2 = forms.CharField(max_length=11, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     validators=[digits_only, starts_with_07], required=False,
                                     label="رقم الهاتف الثاني")
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False,
                             label="البريد الالكتروني")
    dob = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), label="تاريخ الميلاد")
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password1'}),
                               label="كلمة المرور")
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'id_password2'}), label="تأكيد كلمة المرور")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'name',
                    'username',
                    Div(FieldWithButtons('password', StrictButton(content='<i class="fa-solid fa-eye-slash"></i>', type='button',
                                                                  css_class='btn btn-outline-secondary',
                                                                  id='password1Button')),
                        ),
                    Div(FieldWithButtons('confirm_password',
                                         StrictButton(content='<i class="fa-solid fa-eye-slash"></i>', type='button',
                                                      css_class='btn btn-outline-secondary',
                                                      id='password2Button')),
                        ),
                    'province',
                    'dob',
                    'address1',
                    'phone_number_1',
                    'phone_number_2',
                    'email',
                    Submit('submit', 'انشاء', css_class='btn btn-primary login-button'),

                ),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين.")
        try:
            validate_password(password)
        except Exception as e:
            raise forms.ValidationError(e)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    starts_with_07 = RegexValidator(r'^07', 'Field must start with "07".')
    digits_only = RegexValidator(r'^\d{11}$', 'Field must be exactly 11 digits.')

    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label="اسم المستخدم")
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password3'}),
                               label="كلمة المرور")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'username',
                    Div(FieldWithButtons('password', StrictButton(content='<i class="fa-solid fa-eye-slash"></i>', type='button',
                                                                  css_class='btn btn-outline-secondary',
                                                                  id='password3Button')),
                        Submit('submit', 'تسجيل دخول', css_class='btn btn-primary login-button'),
                        ),
                )))
