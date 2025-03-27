from django.urls import path
from . import views
from .views import product_detail  # Import the product_detail view


urlpatterns = [ 
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Add URL pattern for product detail

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
