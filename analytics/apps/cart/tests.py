from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Cart

User = get_user_model()


class TestCart(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(email='ehsan@gmail.com', password='1234567', name='ehsan')

    def test_user_cart(self):
        """Test if cart signal works good"""

        self.assertEqual(Cart.objects.get(user=self.user).id, 1)
        self.assertEqual(self.user.cart, Cart.objects.get(user=self.user))

        self.user.score = 2300
        self.user.discount_percent = 10
        self.user.name = 'ali'
        self.user.save()

        cart = Cart.objects.get(user=self.user)
        cart.price = 1000000
        cart.save()

        self.assertEqual(int(cart.total_price), (cart.price - self.user.discount_value) * self.user.discount_percent)
