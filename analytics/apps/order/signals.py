"""
Important: Celery like other intermediate tools, Only works with open standard data formats like JSON and XML.
So we should only send data in acceptable Serializable formats.
"""
from django.db.models.signals import post_save
from django.core.mail import send_mail

# from .tasks import s_mail


def send_checkout_mail(sender, created, instance, **kwargs):
    """Send mail checkout mail to user to inform him/her about order"""
    if instance.cart.user.email and created:
        # 'delay' method of 'celery' only accepts Serializable objects
        # s_mail.delay(order_id=instance.id)
        send_mail(subject='با تشکر از شما خریدار محترم',
                  message=f'Thanks for choosing us. your order specifications are:'
                          f'Order price: {instance.price},'
                          f'Order price after discount: {instance.total_price},'
                          f'Order ID: {instance.order_id},'
                          f'Order date and time: {instance.ordered_time}',
                  from_email='seller@bigtek.com',
                  recipient_list=['ebikdeli@gmail.com', 'arash@yahoo.com']
                  )


post_save.connect(receiver=send_checkout_mail, sender='order.Order')
