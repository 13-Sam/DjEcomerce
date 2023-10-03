from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import * 
# from .models import Customer
# from . forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)
	# data = json.loads(request.body)
	# productId = data['productId']
	# action = data['action']
	# print('Action:', action)
	# print('Product:', productId)

	# customer = request.user.customer
	# product = Product.objects.get(id=productId)
	# order, created = Order.objects.get_or_create(customer=customer, complete=False)

	# orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	# if action == 'add':
	# 	orderItem.quantity = (orderItem.quantity + 1)
	# elif action == 'remove':
	# 	orderItem.quantity = (orderItem.quantity - 1)

	# orderItem.save()

	# if orderItem.quantity <= 0:
	# 	orderItem.delete()

def singleView(request, pk):
    item = Product.objects.get(id=pk)
    dict = {'item':item}
    return render(request, 'store/single_item.html', context=dict)

def logout_user(request):
    logout(request)
    messages.success(request, 'You are logged out!...')
    return redirect('store')





def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a Customer object associated with the user
            Customer.objects.create(user=user, name=user.username, email=user.email)

            # Log in the user after registration
            login(request, user)
            return redirect('store')  # Replace 'home' with your desired URL
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page (e.g., 'home') after login
            return redirect('store')  # Replace 'home' with your desired URL
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})



