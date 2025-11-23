import unittest
from django.test import TestCase

class BasicTestCase(TestCase):
    def test_unittest_setup(self):
        """Проверка настройки тестов с использованием unittest"""
        self.assertEqual(1 + 1, 2, "Базовая проверка арифметики")
        self.assertTrue(True, "Проверка истинности")