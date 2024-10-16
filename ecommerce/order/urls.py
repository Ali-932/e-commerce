from django.urls import path

from ecommerce.order import views

app_name = 'orders'

urlpatterns = [
    path('delete_order/<int:pk>', views.delete_order, name='delete_order'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('view_orders/', views.view_orders, name='view_orders'),
]
