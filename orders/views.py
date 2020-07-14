from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import decimal

from .models import Pizza, Pasta, Sub, SubExtras, Salads, DinnerPlatters, Toppings, Orders

@login_required
def index(request):
    context = {
        "pizzas" : Pizza.objects.all(),
        "toppings" : Toppings.objects.all(),
        "subs" : Sub.objects.all(),
        "subextras" : SubExtras.objects.all(),
        "pastas" : Pasta.objects.all(),
        "dinnerplatters" : DinnerPlatters.objects.all(),
        "salads" : Salads.objects.all(),
    }
    return render(request, "orders/menu.html", context)

@login_required
def additems(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('index'))

    dish = request.POST["dishtype"]

    if dish in ["regularpizza", "sicilianpizza"]:
        name = request.POST["dishname"]
        size = request.POST["pizza_size"]
        if size == "Small":
            price = request.POST["price_small"]
        else:
            price = request.POST["price_large"]            
        toppings = request.POST.getlist('pizza_topping')
        if(len(toppings) != int(name[0])):
            messages.warning(request, 'Item was not added to the cart! Please ensure that you are adding a correct number of topping(s).')
            return HttpResponseRedirect(reverse('index'))

        remarks = 'Size: ' + size + ' | Toppings: '
        for topping in toppings:
            remarks = remarks + topping + ', '

        remarks = remarks[slice(len(remarks)-1)]
        if dish == 'regularpizza':
            dishtype = 'Regular Pizza'
        else:
            dishtype = 'Sicilian Pizza'

        order = Orders(username = request.user.username, dishtype = dishtype, dishname = name, price = price, remarks = remarks, status = 'Initiated')
        order.save()

        messages.success(request, 'Item was successfully added to the cart! Go to the cart and checkout the order')
        return HttpResponseRedirect(reverse('index'))


    elif dish == "sub":
        name = request.POST["dishname"]
        size = request.POST["sub_size"]
        if size == "Small":
            price = request.POST["price_small"]
        else:
            price = request.POST["price_large"]
        extras = request.POST.getlist('sub_extras')

        remarks = 'Size: ' + size + ' | Extras: ' 
        extra_price = 0
        for extra in extras:
            extra_price += SubExtras.objects.filter(name=extra).first().price
            remarks = remarks + extra + ', '

        remarks = remarks[slice(len(remarks)-1)] # This is not working
        price = decimal.Decimal(price)
        price += extra_price
        order = Orders(username = request.user.username, dishtype = 'Sub', dishname = name, price = price, remarks = remarks, status = 'Initiated')
        order.save()

        messages.success(request, 'Item was successfully added to the cart! Go to the cart and checkout the order')
        return HttpResponseRedirect(reverse('index'))
  

    elif dish == "pasta":
        name = request.POST["dishname"]
        price = request.POST["price"]

        order = Orders(username = request.user.username, dishtype = 'Pasta', dishname = name, price = price, remarks = '', status = 'Initiated')
        order.save()
        
        messages.success(request, 'Item was successfully added to the cart! Go to the cart and checkout the order')
        return HttpResponseRedirect(reverse('index'))


    elif dish == "platter":
        name = request.POST["dishname"]
        size = request.POST["platter_size"]
        if size == "Small":
            price = request.POST["price_small"]
        else:
            price = request.POST["price_large"]

        remarks = 'Size: ' + size
        order = Orders(username = request.user.username, dishtype = 'Dinner Platter', dishname = name, price = price, remarks = remarks, status = 'Initiated')
        order.save()
        
        messages.success(request, 'Item was successfully added to the cart! Go to the cart and checkout the order')
        return HttpResponseRedirect(reverse('index'))


    elif dish == "salad":
        name = request.POST["dishname"]
        price = request.POST["price"]

        order = Orders(username = request.user.username, dishtype = 'Salad', dishname = name, price = price, remarks = '', status = 'Initiated')
        order.save()
        
        messages.success(request, 'Item was successfully added to the cart! Go to the cart and checkout the order')
        return HttpResponseRedirect(reverse('index'))

@login_required
def cart(request):
    orders = Orders.objects.filter(username = request.user.username).filter(status = 'Initiated')
    total_price = 0
    for order in orders:
        total_price += order.price

    context = {
        "orders" : orders,
        "total_price" : total_price,
    }
    return render(request, "orders/cart.html", context)

def checkout(request):

    messages.success(request, 'Your order has been placed successfully!')
    return HttpResponseRedirect('/')

