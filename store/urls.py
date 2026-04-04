from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('api/products/', views.api_products),
    path('api/products/<slug:slug>/', views.api_product_detail),
    path('api/categories/', views.api_categories),
]