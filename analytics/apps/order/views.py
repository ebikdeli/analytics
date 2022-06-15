"""
VERY IMPORTANT NOTE:
    In views, We can't redirect the program directly. We must return url (eg: return reverse(..)) to view function
    then redirect user from function.
    This is it because django router engine searching for path to direct users, only searches views. So if any it
    couldn't find any 'redirect' or 'render' in views or any module pointed to 'urls', Just miss that.
"""

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.cart.models import Cart
from apps.order.models import Order
from .pgi import zarin_pay, zarin_verify


def order(request):
    return HttpResponse('<h1>This is order</h1>')


@login_required
def pay(request):
    """First step of payment. This view redirect user to pgi to enter his/her ID cart"""
    url = zarin_pay(request)
    return redirect(url)


def cart_pay(request):
    """It's the second step towards payment. After payment we should verify if payment was a success or not"""
    url = zarin_verify(request)
    return redirect(url)


@login_required
def receipt(request):
    """The last step toward payment. If every thing goes right user could see his/her order"""
    cart = request.user.cart.first()
    # Create new Order for the user and clean the cart
    Cart.objects.pay(request, cart)
    current_order = Order.objects.filter(cart=cart).first()
    # Or this:: current_order = Order.objects.filter(cart=request.user.cart.first()).first()
    # Or even simpler:: current_order = request.user.cart.first().orders.first()
    return render(request, 'order/templates/order/order_receipt.html', {'order': current_order})
