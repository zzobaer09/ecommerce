##############################################
import json
from .models import *


##########################################################
def cartCookies(request): 
    try:
        cart_cookie = json.loads(request.COOKIES["cart"])
    except: cart_cookie = {}

    orderItem = []
    order = {
        "get_total_item":0,
        "get_total_price":0,
        "shipping":False,
    }
    cartTotalItem = order["get_total_item"]

    for i in cart_cookie:
        try:
            cartTotalItem += cart_cookie[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart_cookie[i]["quantity"]
            order["get_total_price"] +=  total
            order["get_total_item"] += cart_cookie[i]["quantity"]
            item = {
                "product":{
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageUrl": product.imageUrl
                },
                "quantity": cart_cookie[i]["quantity"],
                "get_total": total,
            }
            orderItem.append(item)
            if product.digital == False:
                order["shipping"] = True
        except:
            pass
    return {"allOrder":orderItem , "order":order , "cartTotal":cartTotalItem}

 
###########################################################################
def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,create  = Order.objects.get_or_create(customer=customer , complete=False)
        orderItem = order.orderitem_set.all()
        cartItem = order.get_total_item
    else: 
        cart_cookies = cartCookies(request)
        orderItem = cart_cookies["allOrder"]
        order = cart_cookies["order"]
        cartItem = cart_cookies["cartTotal"]
        
    return {"allOrder":orderItem , "order":order , "cartTotal":cartItem}


######################################################################

def gustOrder(request , data):
    pass