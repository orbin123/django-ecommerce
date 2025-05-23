from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)

    cart_prods = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    return render(request, "cart_summary.html", {"cart_products":cart_prods, "quantities": quantities, "totals": totals})

def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()


        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty':  cart_quantity})
        
        return response
    
    # Return a 400 Bad Request for invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_delete(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product_id = product_id)


        response = JsonResponse({'product': product_id})
        messages.success(request, ("Item is Deleted"))
        return response

def cart_update(request):
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product_id = product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request, ("Item Added to Cart"))
        return response
        
    
