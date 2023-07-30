from django.urls import path

from ecommerce.home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('quality_rep/', views.quality_page, name='quality_rep')
]
