from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create  = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem = order.orderitem_set.all()
        cartItem = order.get_total_item
    else: 
        orderItem = []
        order = {
            "get_total_item":0,
            "get_total_price":0
        }
        cartItem = 0
    products_all_obj = Product.objects.all()
    context = {
        "items":products_all_obj,
        "cartTotal": cartItem,
        "shipping":False,
    }
    return render(request , "store/store.html" , context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create  = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem = order.orderitem_set.all()
        cartItem = order.get_total_item

    else: 
        orderItem = []
        order = {
            "get_total_item":0,
            "get_total_price":0,
            "shipping":False,
        }
        cartItem = 0

        
    context = {"allOrder":orderItem, "order":order,"cartTotal": cartItem,}
    return render(request , "store/cart.html" , context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create  = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem = order.orderitem_set.all()
        cartItem = order.get_total_item

    else: 
        orderItem = []
        order = {
            "get_total_item":0,
            "get_total_price":0,
            "shipping":False,
        }
        cartItem = 0

    context = {"allOrder":orderItem, "order":order,"cartTotal":cartItem,}
    return render(request , "store/checkout.html" , context)


def updateStore(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer , complete=False)
    orderItem  , created = OrderItem.objects.get_or_create(product=product , order=order )
    if action =="add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    orderItem.save()

    
    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse("cart updated", safe=False)



