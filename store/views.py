from django.shortcuts import render
from .models import *

# Create your views here.


def store(request):
    products_all_obj = Product.objects.all()
    context = {
        "items":products_all_obj,
    }
    return render(request , "store/store.html" , context)

def cart(request):
    context = {}
    return render(request , "store/cart.html" , context)


def checkout(request):
    context = {}
    return render(request , "store/checkout.html" , context)


