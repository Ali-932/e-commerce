from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from ecommerce.abstract.models.choices import ProvinceChoices


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username_field: username})

    # def create_user(self, name, email, password=None):
    #     if not email:
    #         raise ValueError('user must have email')
    #
    #     user = self.model(
    #         email=self.normalize_email(email),
    #     )
    #     user.set_password(password)
    #     user.name = name
    #     user.is_active = False
    #     user.save(using=self._db)
    #     return user
    #
    # def create_superuser(self, email, password):
    #     if not email:
    #         raise ValueError('user must have email')
    #
    #     user = self.model(
    #         email=self.normalize_email(email),
    #     )
    #     user.set_password(password)
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user
    #

class User(AbstractUser):
    name = models.CharField('الاسم', max_length=255)
    address1 = models.CharField('العنوان 1', max_length=255)
    phone_number_1 = models.CharField('رقم الهاتف 1',  max_length=11, unique=True)
    phone_number_2 = models.CharField('رقم الهاتف 2', null=True, blank=True, max_length=11)
    username = models.CharField('اسم المستخدم', max_length=255, unique=True)
    dob = models.DateField('تأريخ الميلاد', null=True, blank=True)
    province = models.CharField('المحافظة', max_length=255, choices=ProvinceChoices.choices)

    class Meta:
        verbose_name_plural = 'المستخدمون'
        verbose_name = 'المستخدم'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name}'


