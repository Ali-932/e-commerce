from django.urls import path

from ecommerce.product import views

app_name = 'product'

urlpatterns = [
    path('products/', views.list_products, name='list-products'),
    path('products/<int:pk>', views.product, name='view-product'),
    path('special-offer/', views.list_special_offer_products, name='list-special-offer-products'),
    path('packages/', views.list_package_products, name='list-package-products'),
    path('packages/<int:pk>', views.package, name='view-package')
]
