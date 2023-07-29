from django.urls import path

from ecommerce.home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
]
