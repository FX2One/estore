from django.shortcuts import render
from .models import *
# Create your views here.

def store(request):
    products = Product.objects.all()  # get all the products
    context = {'products': products}  #pass it to template Store.html
    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

