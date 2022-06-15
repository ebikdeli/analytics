from saadati_shop.celery import app
# from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@app.task(name='summ')  # This task used to test the celery
def summ(a, b, c):
    return a + b + c


@app.task(name='send email')
def s_mail(order_id):
    order = Order.objects.get(id=order_id)

    success = send_mail(subject='با تشکر از شما خریدار محترم',
                        message=f'Thanks for choosing us. your order specifications are:'
                                f'Order price: {order.price},'
                                f'Order price after discount: {order.total_price},'
                                f'Order ID: {order.order_id},'
                                f'Order date and time: {order.ordered_time}',
                        from_email='seller@bigtek.com',
                        recipient_list=['ebikdeli@gmail.com', 'arash@yahoo.com']
                        )
    return success
