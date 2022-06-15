from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Cart


@receiver(post_save, sender=get_user_model())
def create_cart(sender, instance, created, **kwargs):
    """Create cart for new created user"""
    if created:
        Cart.objects.create(user=instance)


@receiver(pre_save, sender=Cart)
def count_total_from_user(sender, instance, **kwargs):
    """Count cart total price from user discounts"""
    instance.total_price += instance.price - instance.user.discount_value

    if instance.user.discount_percent:
        instance.total_price *= instance.user.discount_percent
