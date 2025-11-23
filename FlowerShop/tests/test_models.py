# FlowerShop/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from FlowerShop.models import Customer, Order, OrderItem

class ModelTests(TestCase):
    def setUp(self):
        """Настройка данных для тестов"""
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',  # Добавляем username
            password='Test1234'
        )
        self.customer = Customer.objects.create(
            name='Михаил',
            email='mikhail@example.com',
            phone='1234567890',
            address='ул. Тестовая, 1'
        )
        self.order = Order.objects.create(customer=self.customer, status='new')
        self.order_item = OrderItem.objects.create(
            order=self.order,
            flower_name='Роза',
            quantity=2,
            price=100.00
        )

    def test_custom_user_creation(self):
        """Проверка создания CustomUser"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('Test1234'))
        self.assertEqual(str(self.user), 'test@example.com')

    def test_customer_creation(self):
        """Проверка создания Customer"""
        self.assertEqual(self.customer.name, 'Михаил')
        self.assertEqual(self.customer.email, 'mikhail@example.com')
        self.assertEqual(str(self.customer), 'Михаил')

    def test_order_creation(self):
        """Проверка создания Order"""
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.status, 'new')
        self.assertEqual(str(self.order), f"Заказ №{self.order.id} от Михаил")

    def test_order_item_creation(self):
        """Проверка создания OrderItem и метода total_price"""
        self.assertEqual(self.order_item.flower_name, 'Роза')
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 100.00)
        self.assertEqual(self.order_item.total_price(), 200.00)
        self.assertEqual(str(self.order_item), 'Роза — 2 шт.')

    def test_order_total_price(self):
        """Проверка метода total_price у Order"""
        self.assertEqual(self.order.total_price(), 200.00)