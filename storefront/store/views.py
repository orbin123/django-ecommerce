from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Product, Profile
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q 
import json
from cart.cart import Cart


# Category Views
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories": categories})


def category(request, foo):
    foo = foo.replace('-', ' ')  # Replace hyphens with spaces
    try:
        category = Category.objects.get(name__iexact=foo)  # Case-insensitive lookup
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.success(request, "That category doesn't exist")
        return redirect('home')


# Product Views
def product(request, pk):
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, 'product.html', {'product': product, 'categories': categories})


# General Views
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})


# Authentication Views
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Do cart persistence
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert database string into python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add loaded dictionary to update the session
                # Get the cart
                cart = Cart(request)
                # Loop thru the cart and add the items from cart
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials, please try again.')
            return redirect('login')
    else:
        categories = Category.objects.all()
        return render(request, 'login.html', {'categories': categories})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out. Thank you!')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'User Registered! Please Fill Out Your User Info Below...')
            return redirect('update_info')
        else:
            messages.error(request, 'Registration failed. Please try again.')
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                login(request, current_user)
                messages.success(request, "Your profile has been updated!")
                return redirect('home')
        else:
            user_form = UpdateUserForm(instance=current_user)
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.error(request, 'Please log in first.')
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is Form valid
            if form.is_valid():
                form.save()
                messages.error(request, 'Your Password has changed. Please Login again')
                login(request, current_user)
                return redirect('login')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    
    else:
        messages.error(request, 'Please log in first.')
        return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        # Ensure the Profile exists for the current user
        current_user, created = Profile.objects.get_or_create(user=request.user)
        # Getting user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        if created:
            messages.success(request, "A profile has been created for your account.")

        if request.method == 'POST':
            # Bind the form to the POST data and the current user's profile
            form = UserInfoForm(request.POST, instance=current_user)
            # Get user's shipping form
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            if form.is_valid() or shipping_form.is_valid:
                # Original form save
                form.save()
                # Shipping form save
                shipping_form.save()
                messages.success(request, "Your info has been updated!")
                return redirect('home')
        else:
            # Initialize the form with the current user's profile
            form = UserInfoForm(instance=current_user)
            shipping_form = ShippingForm(instance=shipping_user)

        # Render the template with the form
        return render(request, "update_info.html", {'form': form, 'shipping_form': shipping_form})
    else:
        # Redirect to home if the user is not authenticated
        messages.error(request, 'Please log in first.')
        return redirect('home')
    
    # Search

def search(request):
        if request.method == 'POST':
            searched = request.POST['searched']
            # lets query the product db model
            searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

            if not searched:
                messages.success(request, 'That product does not exist... Try again! ')
                return render(request, 'search.html', {})
            else:
                return render(request, 'search.html', {'searched': searched})

        else:
            return render(request, 'search.html', {})
        
        



    