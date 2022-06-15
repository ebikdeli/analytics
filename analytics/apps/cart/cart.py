from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# current user cart got empty and order create
def cart_pay(request):
    cart = request.user.user_cart
    cart.pay()
    messages.success(request, message=_('your order placed successfully'))
    # messages.success(request, message=_('سفارش شما با موفقیت ثبت شد'))
    return cart


def clean_the_cart(request):
    cart = request.user.user_cart
    cart.pay(empty=True)
