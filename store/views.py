from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cartCookies , cartData , gustOrder
###################################################################

#! Create your views here.


def store(request):
    data = cartData(request)
    orderItem = data["allOrder"]
    order = data["order"]
    cartItem = data["cartTotal"]


    products_all_obj = Product.objects.all()
    context = {
        "items":products_all_obj,
        "cartTotal": cartItem,
        "shipping":False,
    }
    return render(request , "store/store.html" , context)

def cart(request):
    data = cartData(request)
    orderItem = data["allOrder"]
    order = data["order"]
    cartItem = data["cartTotal"]

    context = {"allOrder":orderItem, "order":order,"cartTotal": cartItem,}
    return render(request , "store/cart.html" , context)


def checkout(request):
    data = cartData(request)
    orderItem = data["allOrder"]
    order = data["order"]
    cartTotalItem = data["cartTotal"]

    context = {"allOrder":orderItem, "order":order,"cartTotal":cartTotalItem,}
    return render(request , "store/checkout.html" , context)



###############################################################################################################################################################


# other views
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



def processOrder(request):
    data = json.loads(request.body)
    __shipping__ = data["shippingInfo"]
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)

    else:  
        customer , order = gustOrder(request , data) 


########################################################################
    # * global oparations for shipping and complete order
    total  = float(data["UserData"]["total"])
    order.transaction_id = transaction_id
    if total == float(order.get_total_price):
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order=order,
            address=__shipping__["address"],
            city=__shipping__["city"],
            state=__shipping__["state"],
            zipcode=__shipping__["zipcode"],
        )
    



    return JsonResponse("order complete" , safe=False)


