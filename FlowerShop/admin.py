
from django.contrib import admin
from .models import Customer, Order, OrderItem  # импортируем модели

# Простейшая регистрация:
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)