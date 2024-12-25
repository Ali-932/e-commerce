from django.urls import path

from ecommerce.product import views

app_name = 'product'

urlpatterns = [
    path('products/<int:pk>', views.product, name='view-product'),
    path('products/', views.list_products, name='list-products'),
    path('products/manga', views.list_products, name='list-products-manga'),
    path('products/manhwa', views.list_products, name='list-products-manhwa'),
    path('products/comic', views.list_products, name='list-products-comic'),
    path('special-offer/', views.list_special_offer_products, name='list-special-offer-products'),
    path('packages/', views.list_package_products, name='list-package-products'),
]


