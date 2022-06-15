"""
    By default we don't use signals in the order module because it needs Celery to run.
"""
from django.apps import AppConfig
from django.db.models.signals import post_save


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.order'
    
    def ready(self):
        from .signals import send_checkout_mail
        from .models import Order
        order = self.get_model('order')     # <==> Order = self.get_model('Order')
        post_save.connect(receiver=send_checkout_mail, sender='order.order')    # <==> ...sender='Order.order')
    

    """
    # Or we can do ready() method this way:
    def read(self):
        import order.signals <==> from .signals import *
    """
