from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm

class UserCreationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'strong_password_123',
            'password2': 'strong_password_123'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'password1': 'strong_password_123',
            'password2': 'different_password_456'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
