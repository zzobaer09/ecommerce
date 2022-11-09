import json
from .models import *
def cartCookies(request): 
    try:
        cart_cookie = json.loads(request.COOKIES["cart"])
    except: cart_cookie = {}
    print(cart_cookie)

    orderItem = []
    order = {
        "get_total_item":0,
        "get_total_price":0,
        "shipping":False,
    }
    cartItem = order["get_total_item"]

    for i in cart_cookie:
        try:
            cartItem += cart_cookie[i]["quantity"]

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
    return {"allOrder":orderItem , "order":order , "cartTotal":cartItem}
    