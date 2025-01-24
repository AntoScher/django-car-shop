from django.test import SimpleTestCase
from django.urls import reverse, resolve

from shop import views


class UrlsTest(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_car_detail_url_resolves(self):
        url = reverse('car_detail', args=[1])
        self.assertEqual(resolve(url).func, views.car_detail)

    def test_cart_url_resolves(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, views.cart)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add_to_cart', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_payment_confirmation_url_resolves(self):
        url = reverse('payment_confirmation')
        self.assertEqual(resolve(url).func, views.payment_confirmation)
