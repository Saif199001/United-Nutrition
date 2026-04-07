from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register),
    path('api/login/', views.login),
    path('api/products/', views.api_products),
    path('api/products/<slug:slug>/', views.api_product_detail),
    path('api/categories/', views.api_categories),

    # CART
    path('api/cart/', views.get_cart),
    path('api/cart/add/', views.add_to_cart),
    path('api/cart/remove/', views.remove_from_cart),
    path('api/cart/update/', views.update_cart),

    # CHECKOUT
    path('api/checkout/', views.checkout),

    # ORDERS
    path('api/orders/', views.order_history),

    # GALLERY
    path('api/gallery/', views.api_gallery),
]