from django.shortcuts import render, HttpResponse


def shop(request):
    return HttpResponse('<h1>SHOP WORKS PERFECTLY!</h1>')
