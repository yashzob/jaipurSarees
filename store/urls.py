from django.urls import path
from . import views

urlpatterns = [
    # Product CRUD URLs
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:product_id>/edit/', views.product_update, name='product_update'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),

    # E-commerce URLs
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('save-shipping-address/', views.save_shipping_address, name='save-shipping-address'),
    path('payment/', views.payment, name='payment'),
    path('login/', views.login1, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('order-confirmation/', views.process_cod, name='order-confirmation'),
    path('my-orders/', views.my_orders, name='my-orders'),
]
