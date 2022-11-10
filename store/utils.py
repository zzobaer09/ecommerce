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
    ###########################################################
    # * logic for a gust customer
    name =  data["UserData"]["name"]
    email =  data["UserData"]["email"]

    customer , created = Customer.objects.get_or_create(
        email=email
    )

    customer.name = name
    customer.save()

    #############################################################
    # * creating an order
    order = Order.objects.create(customer=customer , complete=False)

    #############################################################
    # * logic for creating OrderItem
    cookie_data = cartCookies(request)
    items = cookie_data["allOrder"]
    for item in items:
        product = Product.objects.get(id=item["product"]["id"])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item["quantity"]
        )
    ################################################################
    return customer , order        