from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)  # Необязательное поле

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# Модель покупателя, оформляющего заказ
class Customer(models.Model):
    name = models.CharField(max_length=100)  # Имя покупателя
    email = models.EmailField()  # Email для связи
    phone = models.CharField(max_length=20, blank=True)  # Телефон (необязательное поле)
    address = models.TextField()  # Адрес доставки

    def __str__(self):
        return self.name  # Отображение имени в списках

# Модель заказа, связанного с покупателем
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')  # Связь с покупателем
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания заказа
    status = models.CharField(  # Статус заказа
        max_length=20,
        choices=[
            ('new', 'Новый'),
            ('processing', 'В обработке'),
            ('shipped', 'Отправлен'),
            ('delivered', 'Доставлен'),
        ],
        default='new'
    )

    def __str__(self):
        return f"Заказ №{self.id} от {self.customer.name}"  # Отображение в списке заказов

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())  # Сумма всех позиций в заказе

# Модель позиции в заказе — конкретный букет или цветок
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # Связь с заказом
    flower_name = models.CharField(max_length=100)  # Название цветка или букета
    quantity = models.PositiveIntegerField()  # Количество единиц
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Цена за одну единицу (например, букет)

    def __str__(self):
        return f"{self.flower_name} — {self.quantity} шт."  # Отображение в списке

    def total_price(self):
        return self.quantity * self.price  # Метод для вычисления общей стоимости позиции
