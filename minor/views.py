import json

from django.db.models.functions import datetime

from .utils import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import logout
from django.http import JsonResponse

# Create your views here.
def index(request):
    Data = cartData(request)
    cartItems = Data['cartItems']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }
    return render(request, 'index.html', context)

def store(request):
    products = Product.objects.all()
    Data = cartData(request)
    cartItems = Data['cartItems']
    context = {
        'products': products,
        'cartItems': cartItems
    }
    return render(request, 'store.html', context)

def cart(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    context = {
        'items': items,
        'orders': order,
        'cartItems': cartItems
    }
    return render(request, 'cart.html', context)

def checkout(request):
    Data = cartData(request)
    cartItems = Data['cartItems']
    order = Data['order']
    items = Data['items']

    context = {
        'items': items,
        'orders': order,
        'cartItems': cartItems
    }
    return render(request, 'checkout.html', context)

def login(request):
    if request.method == 'POST':
        u_name = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=u_name, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, "incorrect Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        u_name = request.POST['user_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']
        if f_name != "" and l_name != "" and email != "" and pass1 != "" and pass2 != "":
            if pass1==pass2:
                if User.objects.filter(username=u_name).exists():
                    messages.info(request, 'User Name Exist')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Exist')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=u_name, password=pass1, email=email, first_name=f_name, last_name=l_name )
                    user.save()
                    return redirect('/')
        else:
            messages.info(request, 'please Fill Form Completely')
            return redirect('register')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('ProductId: ', productId)
    print('Action ', action)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItems, created = OrderItems.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItems.quantity = (orderItems.quantity + 1)
    elif action == 'remove':
        orderItems.quantity = (orderItems.quantity - 1)

    orderItems.save()

    if orderItems.quantity <= 0:
        orderItems.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = "True"

    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            phone=data['shipping']['phone'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            pincode=data['shipping']['pincode'],
        )

    return JsonResponse('payment Complete', safe=False)

def detail(request, product_id):
    product = Product.objects.get(pk = product_id)
    Data = cartData(request)
    cartItems = Data['cartItems']
    context = {
        'product': product,
        'cartItems': cartItems,
    }
    return render(request, 'detail.html', context)

