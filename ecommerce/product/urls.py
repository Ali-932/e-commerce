from django.urls import path

from ecommerce.product import views

app_name = 'product'

urlpatterns = [
    path('products/', views.list_products, name='list-products'),
]
