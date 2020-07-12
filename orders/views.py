from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Pizza, Pasta, Sub, SubExtras, Salads, DinnerPlatters, Toppings

@login_required
def index(request):
    context ={
        "pizzas" : Pizza.objects.all(),
        "toppings" : Toppings.objects.all(),
        "subs" : Sub.objects.all(),
        "subextras" : SubExtras.objects.all(),
        "pastas" : Pasta.objects.all(),
        "dinnerplatters" : DinnerPlatters.objects.all(),
        "salads" : Salads.objects.all(),
    }
    return render(request, "orders/menu.html", context)
