from django.db import models
from django.utils.translation import gettext_lazy as _

# Because of circular Import Error, We better use "to='<app_label>.Model'"
# from cart.models import Cart


class Order(models.Model):
    # We better not use 'Cart' model directly because of 'circular Import Error'
    cart = models.ForeignKey(to='cart.Cart',
                             related_name='orders',
                             on_delete=models.CASCADE,
                             verbose_name=_('cart'))
    order_id = models.CharField(verbose_name=_('order id'), max_length=10, unique=True)
    items = models.JSONField(verbose_name=_('order items'), blank=True, null=True)
    products = models.ManyToManyField('shop.Product', related_name='order_products')
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=0, default=0)
    total_price = models.DecimalField(verbose_name=_('total price'), max_digits=10, decimal_places=0, default=0)
    total_items = models.PositiveIntegerField(default=0, verbose_name=_('total items'))
    ordered_time = models.DateTimeField(verbose_name=_('ordered time'), auto_now_add=True)
    authority = models.CharField(verbose_name=_('authority code'), max_length=40, blank=True, null=True)
    is_success = models.BooleanField(verbose_name=_('successfully paid'), default=False)
    is_active = models.BooleanField(verbose_name=_('order is active'), default=False)
    updated = models.DateTimeField(verbose_name=_('updated'), auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.order_id
