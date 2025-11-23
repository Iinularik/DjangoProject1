from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from FlowerShop.models import Customer, Order, OrderItem

class InterfaceTests(TestCase):
    def setUp(self):
        """Настройка данных и клиента для тестов"""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
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

    def test_login_page(self):
        """Проверка страницы входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Вход в систему')
        self.assertContains(response, 'Email:')
        self.assertContains(response, 'Пароль:')
        self.assertContains(response, 'Зарегистрируйтесь')

    def test_register_page(self):
        """Проверка страницы регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Регистрация')
        self.assertContains(response, 'Email:')
        self.assertContains(response, 'Имя пользователя')
        self.assertContains(response, 'Пароль:')
        self.assertContains(response, 'Подтверждение пароля')
        self.assertContains(response, 'Войти')

    def test_order_list_page_authenticated(self):
        """Проверка страницы заказов для авторизованного пользователя"""
        self.client.login(email='test@example.com', password='Test1234')
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Flower_Shop/order_list.html')  # Исправлено: Flower_Shop
        self.assertContains(response, 'Привет, test@example.com')
        self.assertContains(response, 'Выйти')
        self.assertContains(response, 'Список заказов')
        self.assertContains(response, 'Михаил')
        self.assertContains(response, 'Роза — 2 шт.')
        self.assertContains(response, '200.00 руб.')

    def test_order_list_page_unauthenticated(self):
        """Проверка перенаправления неавторизованного пользователя"""
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/orders/')

    def test_logout_page(self):
        """Проверка страницы выхода"""
        self.client.login(email='test@example.com', password='Test1234')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Исправлено: ожидается перенаправление
        self.assertRedirects(response, '/accounts/login/')  # Проверяем перенаправление