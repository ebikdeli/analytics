"""
    This code writen for ZarinPal pgi, but we can use it for any REST pgi service with minimal changes
"""

from django.conf import settings
from django.contrib import messages
from django.shortcuts import reverse

import requests
import json


# This is local callback url
CALLBACK_URL = 'http://127.0.0.1:8000/order/cart_pay/'
if not settings.DEBUG:
    # This is website callback url
    CALLBACK_URL = 'https://www.example/order/cart_pay/'
ZARIN_MERCHANT_ID = 'b46922ec-f436-402b-a553-4107451475cc'


def zarin_response_code(request, zarin_response):
    """Helper function to decode if any error messages in payment process"""
    code = zarin_response['errors']['code']
    if code == -9:
        messages.error(request, 'موجودی باید بیش از 100 ریال بشد')
    elif code == -10:
        messages.error(request, 'آدرس آی پی یا مرچنت کد پذیرنده صحیح نیست')
    elif code == -12:
        messages.error(request, 'تلاش بیش از اندازه در یک بازه زمانی کوتاه. بعدا تلاش کنید')
    elif code == -34:
        messages.error(request, 'مبلغ وارد شده از تراکنش بیشتر است')
    elif code == -51:
        messages.error(request, 'پرداخت ناموفق')
    elif code == -53:
        messages.error(request, 'کد اتوریتی نامعتبر است')


def zarin_pay_verify(request, authority):
    """Helper function used to verify the payment"""
    url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
    data = {
        'merchant_id': ZARIN_MERCHANT_ID,
        # 'amount': int(cart.total_price * 100),
        'amount': 1000,
        'authority': authority
            }
    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    r = requests.post(url=url, data=json.dumps(data), headers=headers)
    if r.status_code == 200 or 201:
        zarin_response = r.json()
        if zarin_response['data']:
            messages.success(request, f'تاییدیه تراکنش شما: {authority}')
        else:
            zarin_response_code(request, zarin_response)


def zarin_pay(request):
    """Initialize payment process and redirect user to pgi"""
    user = request.user
    cart = user.cart.first()
    if not user.email:
        user.email = 'ثبت نشده'
    if not user.phone:
        user.phone = 'ثبت نشده'
    url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
    headers = {'accept': 'application/json',
               'content-type': 'application/json'}
    data = {
        'merchant_id': ZARIN_MERCHANT_ID,
        # 'amount': int(cart.total_price * 10),
        'amount': 1000,
        'description': f'خرید از فروشگاه سعادتی',
        'callback_url': CALLBACK_URL,
        'metadata': {'email': user.email,
                     'phone': user.phone}
            }
    try:
        r = requests.post(url=url, data=json.dumps(data), headers=headers)
    except requests.ConnectionError:
        messages.error(request, 'برقراری با ارتباط با واسط پرداخت به مشکل برخورده')
        return reverse('cart:show_cart')
    if r.status_code == 200 or 201:
        zarin_response = r.json()
        # If request was a success:
        if zarin_response['data']:
            authority = zarin_response['data']['authority']
            new_url = f'https://www.zarinpal.com/pg/StartPay/{authority}'
            # Redirect user to PGI to pay
            return new_url
        # If there is a error:
        else:
            zarin_response_code(request, zarin_response)
            return reverse('cart:cart_view')
    else:
        messages.add_message(request, messages.ERROR, 'ارتباط با سایت پذیرنده ممکن نمی باشد')
    return reverse('cart:cart_view')


def zarin_verify(request):
    """Used in the last step to verify the payment then redirect user to receipt"""
    data = request.GET
    cart = request.user.cart.first()
    authority = data['Authority']
    cart.authority = data['Authority']
    cart.save()
    # Helper method called
    zarin_pay_verify(request, authority)
    if data['Status'] == 'OK':
        messages.success(request, 'سفارش شما با موفقیت ثبت شد.')
        return reverse('order:receipt')
    if data['Status'] == 'NOK':
        messages.add_message(request, messages.SUCCESS, 'پرداخت انجام نگرفت و سفارشی ثبت نگردید')
        return reverse('cart:show_cart')


"""
    Note that we should not use 'redirect' function in helper modules. Else we get
    ValueError None type object error.
"""
