from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import decimal


@receiver(pre_save, sender='shop.Product')
def calculate_product_end_price(sender, instance, **kwargs):
    """Calculate 'end_price' for product after enforcing product discounts"""
    percent_value = decimal.Decimal(0)
    if instance.discount_percent:
        if instance.discount_percent < 0:
            raise ValidationError(_('discount percent could not be less than 0'))
        elif instance.discount_percent > 100:
            raise ValidationError(_('discount percent could not be more than 100'))
        percent_value += instance.price * (instance.discount_percent / 100)
    instance.end_price = instance.price - (instance.discount_value + percent_value)


@receiver(pre_save, sender='shop.Product')
def available_stock_items(sender, instance, **kwargs):
    """If items in stock more than zero assign 'available' to 'True'"""
    if instance.in_stock > 0:
        instance.is_available = True
    else:
        instance.is_available = False
