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

        remarks = remarks[slice(len(remarks)-2)]
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

        if len(extras) > 0:
            remarks = 'Size: ' + size + ' | Extras: '
        else:
            remarks = 'Size: ' + size + '  '
        
        extra_price = 0
        for extra in extras:
            extra_price += SubExtras.objects.filter(name=extra).first().price
            remarks = remarks + extra + ', '

        remarks = remarks[slice(len(remarks)-2)]
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

@login_required
def checkout(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/')

    orders = Orders.objects.filter(username = request.user.username).filter(status = 'Initiated')

    for order in orders:
        order.status = 'Paid'
        order.save()

    messages.success(request, 'Your order has been placed successfully!')
    return HttpResponseRedirect(reverse('myorders'))

@login_required
def allorders(request):
    if request.user.is_superuser:
        orders = Orders.objects.all().order_by('id').reverse()
        context = {
            "orders" : orders
        }
        return render(request, "orders/allorders.html", context)
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required
def complete(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/')
    
    order_id = request.POST["order"]
    order = Orders.objects.get(pk=order_id)
    order.status = 'Delivered'
    order.save()
    
    return HttpResponseRedirect(reverse('allorders'))

@login_required
def myorders(request):
    ongoing_orders = Orders.objects.filter(username = request.user.username).filter(status = 'Paid').order_by('id').reverse()
    previous_orders = Orders.objects.filter(username = request.user.username).filter(status = 'Delivered').order_by('id').reverse()

    context = {
        "ongoing_orders" : ongoing_orders,
        "previous_orders" : previous_orders,
    }
    return render(request, "orders/myorders.html", context)


