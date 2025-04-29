from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        # Logic 
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            # Convert string elements to integer
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = int(quantity)
        
        # Logic - Update quantity if product already exists in cart
        if product_id in self.cart:
            self.cart[product_id] += product_qty
        else:
            self.cart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            # Convert string elements to integer
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        # Count the total quantity of all items in cart
        if not self.cart:  # Check if cart is empty
            return 0
        return sum(self.cart.values())
    
    def get_prods(self):
        # Get ids from cart
        product_id = self.cart.keys()

        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_id)

        # Return those looked up products
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def cart_total(self):
        quantities = self.cart
        product_ids = quantities.keys()
        products = Product.objects.filter(id__in = product_ids)
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id ==key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)         
        return total  


    def update(self, product_id, quantity):
        product_id = str(product_id)
        product_qty = int(quantity)
        # Get Cart
        our_cart = self.cart
        # Update Dictionary/cart
        our_cart[product_id] = product_qty

        self.session.modified = True

         # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            # Convert string elements to integer
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


        thing = self.cart
        return thing
    
    def delete(self, product_id):

        product_id = str(product_id)

        # Delete from the dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

         # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            # Convert string elements to integer
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))




