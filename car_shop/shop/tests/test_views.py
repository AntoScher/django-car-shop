from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shop.models import Car


class HomeViewTest(TestCase):

    def setUp(self):
        Car.objects.create(
            name='Test Car',
            description='Test Description',
            price=10000.00
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_context(self):
        response = self.client.get(reverse('home'))
        self.assertIn('cars', response.context)
        self.assertEqual(len(response.context['cars']), 1)




class CarDetailViewTest(TestCase):

    def setUp(self):
        self.car = Car.objects.create(
            name='Test Car',
            description='Test Description',
            price=10000.00
        )

    def test_car_detail_view_status_code(self):
        response = self.client.get(reverse('car_detail', args=[self.car.id]))
        self.assertEqual(response.status_code, 200)

    def test_car_detail_view_template(self):
        response = self.client.get(reverse('car_detail', args=[self.car.id]))
        self.assertTemplateUsed(response, 'car_detail.html')

    def test_car_detail_view_context(self):
        response = self.client.get(reverse('car_detail', args=[self.car.id]))
        self.assertIn('car', response.context)
        self.assertEqual(response.context['car'], self.car)


class CartViewTest(TestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('cart'))
        self.assertRedirects(response, '/login/?next=/cart/')

    def test_access_for_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')


class AddToCartViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.car = Car.objects.create(
            name='Test Car',
            description='Test Description',
            price=10000.00
        )

    def test_add_to_cart_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_to_cart', args=[self.car.id]))
        self.assertRedirects(response, reverse('cart'))

