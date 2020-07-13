from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.additems, name="additems"),
    path("cart/", views.cart, name="cart")
]
