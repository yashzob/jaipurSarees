from django.urls import path

from . import views

urlpatterns = [
    path('reg', views.register, name='register'),
    path('', views.home, name='home'),
    # path('otp/<str:uid>/', views.otpVerify, name='otp'),
    path('otp/<uuid:uid>/', views.otpVerify, name='otp'),
    path('pp', views.test, name='test'),

]