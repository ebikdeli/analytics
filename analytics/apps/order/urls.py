from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path('order/', views.order, name='order'),
    path('pay/', views.pay, name='pay'),
    # path('verify/', views.verify, name='verify'),
    path('cart_pay/', views.cart_pay, name='cart_pay'),
    path('receipt/', views.receipt, name='receipt')
]
