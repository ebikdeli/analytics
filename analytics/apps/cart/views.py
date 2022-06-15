from django.shortcuts import HttpResponse


def cart_view(request):
    return HttpResponse('<h1>You can see the cart</h1>')
