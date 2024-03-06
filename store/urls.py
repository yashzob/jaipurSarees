from django.urls import path
from . import views

urlpatterns = [
    # Leave as an empty string for the base URL
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('save-shipping-address/', views.save_shipping_address, name='save-shipping-address'),
    path('payment/', views.payment, name='payment'),
    path('login/', views.login1, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register',views.register,name='register'),
]

