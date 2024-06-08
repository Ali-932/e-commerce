from django.urls import path

from ecommerce.product import views

app_name = 'product'

urlpatterns = [
    path('products/', views.list_products, name='list-products'),
    path('special-offer/', views.list_special_offer_products, name='list-special-offer-products'),
    path('products/<int:pk>', views.product, name='view-product'),
]
