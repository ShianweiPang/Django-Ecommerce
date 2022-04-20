from ctypes import addressof
import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from numpy import product
from .models import *
import json
from .utils import cartData, cookieCart, guestOrder

# for userCreation
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages

# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+user)
            return redirect('login')

    context={'form':form}
    return render(request, 'store/register.html',context)

def login(request):
    context={}
    return render(request, 'store/login.html',context)

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    order_products = data['order_products']
    order =  data['order']

    context = {'order_products':order_products, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    order_products = data['order_products']
    order =  data['order']

    context = {'order_products':order_products, 'order':order}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # print(action, productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, cart_complete=False)
    # order_products = order.order_product_set.all()
    order_product, created = Order_Product.objects.get_or_create(order=order, product=product)

    if action=="add":
        order_product.quantity +=1
    elif action =="remove":
        order_product.quantity -=1
    order_product.save()
    cart_total = order.get_total_quantity
    cart_totalPrice = order.get_total_price
    
    if order_product.quantity<=0:
        order_product.delete()
    # print(order_product.quantity, order_product.product.name)

    return JsonResponse({'cart_total':cart_total,'cart_totalPrice':cart_totalPrice,'quantity':order_product.quantity, 'unitprice':order_product.product.price}, safe=False)


def process_order(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, cart_complete=False)

    else:
        order = guestOrder(request, data)
        

    total = float(data['userFormData']['total'])
    order.transaction_id = transaction_id
    # print(total, order.get_total_price)
    # check the total from the front end is it same as from the backend
    if total==order.get_total_price:
        order.cart_complete = True
    order.save()

    if order.shipping == True:
        Shipping.objects.create(
            order= order,
            address= data['shippingInfo']['address'],
            city= data['shippingInfo']['city'],
            state= data['shippingInfo']['state'],
            zipcode= data['shippingInfo']['zipcode'],
        )   
    return JsonResponse('Payment submitted', safe=False)



