from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
path('register/', views.register, name='register'),
]
