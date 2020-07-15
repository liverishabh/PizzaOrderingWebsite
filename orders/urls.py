from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.additems, name="additems"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("allorders/", views.allorders, name="allorders"),
    path("complete/", views.complete, name="complete"),
    path("myorders/", views.myorders, name="myorders")
]
