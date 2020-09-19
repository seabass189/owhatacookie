from django.shortcuts import render, get_object_or_404
from .models import Category, Item
from decimal import *

def home(request):
    context = {
    'num_of_items': get_session_cart_size(request.session.get('cart')),
    }
    return render (request, 'items/home.html', context=context)

def items_list(request):
    context = load_items_list(request)
    return render (request, 'items/items_list.html', context=context)

def load_items_list(request):
    category_list = Category.objects.all()
    category_items = []
    category_names = []
    for category in category_list:
        category_names.append(category.name)
        items = list(Item.objects.filter(category_id=category.id))
        category_items.append(items)
    context = {
    'category_names': category_names,
    'category_items': category_items,
    'i_amt': range(len(category_names)),
    'num_of_items': get_session_cart_size(request.session.get('cart')),
    }
    return context

# def get_cart_subtotal(cart):
#     subtotal = 0
#     item_list = cart.get('details').get('item_id_list')
#     for item_id in item_list:
#         item_price = cart.get(str(item_id)).get('item').get('price')
#         item_quantity =  cart.get(str(item_id)).get('quantity')
#         subtotal += float(item_price) * item_quantity
#     subtotal = Decimal(subtotal).quantize(Decimal('0.01'))
#     return subtotal

# SESSION CART FUNCTIONS
def add_to_session_cart(request, id):
    item = get_object_or_404(Item, id=id)
    quantity = int(request.POST['quantity' + str(item.id)])
    cart = request.session.get('cart')
    if cart:
        # cart exists
        order_item = cart.get(str(item.id))
        if order_item == None:
            # item does not exist in cart
            order_item_details = {
            'quantity': quantity,
            'item': item.get_dict_of_model(),
            }
            list = cart.get('details').get('item_id_list')
            list.append(str(item.id))
            cart['details']['item_id_list'] = list
            cart[str(item.id)] = order_item_details
        else:
            # item exists, update item_quantity
            prev_quantity = cart.get(str(item.id)).get('quantity')
            cart[str(item.id)]['quantity'] = prev_quantity + quantity
        request.session['cart'] = cart
        message = 'Cart updated.'
    else:
        # cart does not exist, create cart
        request.session['cart'] = {}
        order_details = {
        'item_id_list': [item.id,],
        }
        order_item_details = {
        'quantity': quantity,
        'item': item.get_dict_of_model(),
        }
        request.session['cart']['details'] = order_details
        request.session['cart'][str(item.id)] = order_item_details
        message = 'Cart updated.'
    context = load_items_list(request)
    context['message'] = message
    context['num_of_items'] = get_session_cart_size(request.session.get('cart'))
    return render(request, 'items/items_list.html',context = context)

def session_cart(request):
    context = {}
    cart = request.session.get('cart')
    if cart:
        if request.method == 'POST':
            print(request.POST)
            item_list = cart.get('details').get('item_id_list')
            for item_id in item_list:
                if ('item_note' + str(item_id)) in request.POST:
                    item_note = request.POST['item_note' + str(item_id)]
                    cart[str(item_id)]['note'] = item_note
                if ('quantity' + str(item_id)) in request.POST:
                    quantity = int(request.POST['quantity' + str(item_id)])
                    if quantity == 0:
                        cart.pop(str(item_id))
                        item_list.remove(item_id)
                    else:
                        item = cart.get(str(item_id))
                        item['quantity'] = quantity
                        cart[str(item_id)] = item_list
            cart['details']['item_id_list'] = item_list
            if 'instructionBox' in request.POST:
                order_note = request.POST['instructionBox']
                cart['details']['note'] = order_note
            request.session['cart'] = cart
        cart_size = get_session_cart_size(request.session.get('cart'))
        context['num_of_items'] = cart_size
        if cart_size < 1:
            request.session.pop('cart')
            context = {
            'message': 'You do not have a pending order',
            'num_of_items': 0,
            }
            return context
        # context['order_subtotal'] = get_cart_subtotal(cart)
        item_ids = cart.get('details').get('item_id_list')
        order_items = []
        for id in item_ids:
            item = Item.objects.get(id=id)
            item_dict = {
            'item': item,
            'quantity': cart.get(str(item.id)).get('quantity')
            }
            if cart.get(str(item.id)).get('note'):
                item_dict['note'] = cart.get(str(item.id)).get('note')
            print('\nITEM DICT FOR ', id, ": ", item_dict, "\n")
            order_items.append(item_dict)
        if cart.get('details').get('note'):
            context['order_node'] = cart.get('details').get('note')
        context['order_items'] = order_items
    else:
        context['message'] = 'You do not have a pending order'
    return render(request, 'items/cart.html', context=context)

def get_session_cart_size(cart):
    size = 0
    if cart:
        print('\nCART: ', cart ,'\n')
        item_list = cart.get('details').get('item_id_list')
        for item_id in item_list:
            item_quantity =  cart.get(str(item_id)).get('quantity')
            size += item_quantity
    return size
