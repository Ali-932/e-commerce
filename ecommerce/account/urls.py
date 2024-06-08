
from django.urls import path

from ecommerce.account import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_user, name='logout')
]
