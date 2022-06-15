from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

### This code is coupled with 'order' module 
from apps.order.models import Order

def generate_random_id():
    """To create random number for 'Order' 'order_id' field"""
    import random
    import string
    s = 10  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=s))
    return ran

class CartManager(models.Manager):
    def cart_clear(self, cart, user):    # This is last operation on cart
        """
            This manager method clear cart after transaction received or
            after user cleared his/her cart without any transaction.
            You can change this code anyway you want.
        """

        def user_save(user_obj, cart_obj, score_changer=1000):
            """Change user score if user buy something"""
            # By default every 1000 Toman is 1 score
            user_obj.score = cart_obj.total_price / score_changer
            user_obj.save()
        
        def order_create(cart_obj):
            """To create new order in db"""
            Order.objects.create(cart=cart_obj,
                                 order_id=generate_random_id(),
                                 ### This field receive any items or services bought by user in cart
                                 total_paid=cart_obj.total_price,
                                 price=cart_obj.price,
                                 total_items = cart_obj.total_items,
                                 authority=cart_obj.authority,
                                 is_success=True,
                                 is_active=True)

        def cart_disappear(cart_obj):
            """Clear user cart after successful transaction or clear cart request"""
            cart_obj.price = 0
            cart_obj.total_price = 0
            cart_obj.total_items = 0
            cart_obj.is_paid = False
            cart.authority = None
            cart_obj.save()

        qs = self.get_queryset().filter(id=cart.id)
        if qs:
            cart = qs.last()
            
            # If user complete his/her transaction. By the way cart get cleared wether user buy something or not
            if cart.is_paid:
                user_save(user, cart)
                order_create(cart)
            cart_disappear(cart)
            return True
 
        return None


class Cart(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', verbose_name=_('user'))
    """This line should be filled with some filed representing items or services user selected"""
    price = models.DecimalField(default=0, decimal_places=0, max_digits=9, verbose_name=_('total price'))
    total_price = models.DecimalField(default=0, decimal_places=0, max_digits=9, verbose_name=_('total price after discount'))
    total_items = models.IntegerField(default=0, verbose_name=_('total items'))
    is_paid = models.BooleanField(default=False, verbose_name=_('paid'))
    authority = models.CharField(verbose_name=_('authority code'), max_length=40, blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)

    objects = CartManager()

    class Meta:
        ordering = ['-updated']

    def __str__(self) -> str:
        return f'{self.user.email}_cart'

    ### Technically we don't need this method because 'self' is current model instance
    def get_object(self):
        """Helper method to get current instance of cart object"""
        return Cart.objects.get(id=self.id)

    def pay(self, empty=None):
        cart = self.get_object()    # <==> cart = self
        self.is_paid = True

        if empty is not None:       # If we want to empty cart without order
            self.is_paid = False

        self.save()
        Cart.objects.cart_clear(cart=cart, user=cart.user)      # OR: Cart.objects.cart_clear(cart=self, user=self.user)


"""
In Model methods, 'self' means current model instance.
for example in above:
    current_cart = self = self.get_object()
"""
