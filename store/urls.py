from django.urls import path
from . import views
urlpatterns = [
    path("" , views.store , name="store"),
    path("cart/" , views.cart , name="cart"),
    path("checkout/", views.checkout , name="checkout"),

    # other urls
    path("update_store/" , views.updateStore , name="updateStore"),
    path("process_order/" , views.processOrder , name="processOrder"),
]
