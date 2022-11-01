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
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create  = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem = order.orderitem_set.all()
    else: 
        orderItem = []
        order = {
            "get_total_item":0,
            "get_total_price":0
        }
    context = {"allOrder":orderItem, "order":order}
    return render(request , "store/cart.html" , context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create  = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem = order.orderitem_set.all()
    else: 
        orderItem = []
        order = {
            "get_total_item":0,
            "get_total_price":0
        }
        
    context = {"allOrder":orderItem, "order":order}
    return render(request , "store/checkout.html" , context)


