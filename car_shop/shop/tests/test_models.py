from django.contrib.auth.models import User
from django.test import TestCase

from shop.models import Car, Order


class CarModelTest(TestCase):

    def setUp(self):
        self.car = Car.objects.create(
            name='Test Car',
            description='Test Description',
            price=10000.00
        )

    def test_car_creation(self):
        self.assertEqual(self.car.name, 'Test Car')
        self.assertEqual(self.car.description, 'Test Description')
        self.assertEqual(self.car.price, 10000.00)

    def test_car_str_representation(self):
        self.assertEqual(str(self.car), 'Test Car')




class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.car = Car.objects.create(
            name='Test Car',
            description='Test Description',
            price=10000.00
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=10000.00
        )
        self.order.cars.add(self.car)

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertIn(self.car, self.order.cars.all())
        self.assertEqual(self.order.total_price, 10000.00)
        self.assertEqual(self.order.status, 'pending')
