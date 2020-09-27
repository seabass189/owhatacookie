from django.shortcuts import render
from items import views as items_views

def session_checkout(request):
    # context = {}
    # cart = request.session.get('cart')
    # if cart:
    #     subtotal = get_cart_subtotal(cart)
    #     fees = get_cart_fees(subtotal)
    #     order_list = get_bill_dict(cart)
    #     total = subtotal + fees['Sales Tax'] # TODO: check this fees stuff
    #     context

    context = {
    'num_of_items': items_views.get_session_cart_size(request.session.get('cart')),
    }
    return render (request, 'checkout.html', context=context)

def get_cart_subtotal(cart):
    subtotal = 0
    item_list = cart.get('details').get('item_id_list')
    for item_id in item_list:
        item_price = cart.get(str(item_id)).get('item').get('price')
        item_quantity =  cart.get(str(item_id)).get('quantity')
        subtotal += float(item_price) * item_quantity
    subtotal = Decimal(subtotal).quantize(Decimal('0.01'))
    return subtotal

def get_cart_fees(subtotal):
    fees = {
    "Sales Tax": Decimal(float(subtotal) * 0.09).quantize(Decimal('0.01')),
    "Shipping Fee": Decimal('10.00'),
    "Service Fee": Decimal('5.00')
    }
    return fees
