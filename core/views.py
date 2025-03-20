from django.shortcuts import render , get_object_or_404 , redirect
from .models import *
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def create_user_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email    = request.POST["email"]
        password = request.POST["password"]

        if not username:
            messages.error(request, "Username field cannot be empty")
        elif not email:
            messages.error(request, "Email field cannot be empty")
        elif not password:
            messages.error(request, "Password field cannot be empty")
        else:
            user         = User.objects.create_user(
                username = username,
                email    = email,
                password = password
            )
            user.save()
            return redirect('login')
    return render(request, 'core/register.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user     = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'core/login.html')

def product_list(request):
    products = Product.objects.all().select_related()
    return render(request, 'core/products.html', {'products':products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'core/product_detail.html', {'product':product})

def products_by_category(request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category)
        return render(request, 'core/products.html', {'products': products, 'category': category})

@login_required(login_url='login')
def add_to_cart(request, product_id) :
    product          = get_object_or_404(Product, pk=product_id)
    current_customer = request.user.customer
    try:
        cart_item    = CartItem.objects.get(
            product  = product,
            customer = current_customer
        )
        cart_item.quantity += 1
        cart_item.save()
    except:
        cart_item    = CartItem.objects.create(
            product  = product,
            customer = current_customer,
            quantity = 1
        )
        cart_item.save()
        messages.success(request, "Product added to cart")
    return redirect('product_list')

@login_required(login_url='login')
def remove_from_cart(request, product_id) :
    product          = get_object_or_404(Product, pk=product_id)
    current_customer = request.user.customer
    cart_item        = CartItem.objects.get(product=product, customer=current_customer)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def cart(request) :
    current_customer = request.user.customer
    cart_items       = CartItem.objects.filter(customer=current_customer)
    return render(request, 'core/cart.html', {'cart_items':cart_items})

@login_required(login_url='login')
def increase_quantity(request, product_id) :
    product          = get_object_or_404(Product, pk=product_id)
    current_customer = request.user.customer

    cart_item        = CartItem.objects.get(
            product  = product,
            customer = current_customer
        )
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def decrease_quantity(request, product_id) :
    product          = get_object_or_404(Product, pk=product_id)
    current_customer = request.user.customer
    
    cart_item        = CartItem.objects.get(
        product      = product,
        customer     = current_customer
    )
    if  cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else :
        cart_item.delete()
    return redirect('cart')    

def passing_order_view(request):
    customer = request.user.customer
    items    = CartItem.objects.filter(customer=customer)
    order    = Order.objects.get(customer=customer)
    order.items.add(*items)
    order.save()
    return HttpResponse("created")
