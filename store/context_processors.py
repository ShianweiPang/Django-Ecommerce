import json
from .models import Order, Order_Product, Product

def get_total_quantity(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, cart_complete=False)
        
        if order:
            orderitems = Order_Product.objects.filter(order=order)
            cart_total = sum([item.quantity for item in orderitems])
        else:
            cart_total=0

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}
        cart_total = 0

        try:
            for product_id in cart.copy():
                cart_total += cart[product_id]['quantity']
                product = Product.objects.get(id=product_id)
        except:
            print("ERROR: Missing item")
            pass
                

    return {'cart_total':cart_total}