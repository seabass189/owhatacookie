from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.shortcuts import render
from django.utils import timezone
from items import views as items_views
from items.models import Item
from customers.models import Customer, Address
from orders.models import Order, OrderItem
from .forms import CheckoutForm
from decimal import *
from owhatacookie import settings
import random
import string

debug = True

def session_checkout(request):
    if debug: print('\n Entering view function \n')
    if debug: print('\n ', request.POST, ' \n')
    context = {}
    cart = request.session.get('cart')
    if cart:
        if debug: print('\n Cart exists \n')
        form = CheckoutForm
        subtotal = get_cart_subtotal(cart)
        fees = get_cart_fees(subtotal)
        order_list = get_bill_dict(cart)
        total = subtotal + fees['Sales Tax'] # TODO: check this fees stuff
        context = {
        'num_of_items': items_views.get_session_cart_size(cart),
        'form': form,
        'fees': fees,
        'subtotal': subtotal,
        'order_list': order_list,
        'total': total,
        }
        if debug: print('\n Got context \n')
        if request.method == 'GET':
            if debug: print('\n Return GET \n')
            return render (request, 'checkout.html', context=context)
        elif request.method == 'POST':
            form = CheckoutForm(request.POST or None)
            if form.is_valid():
                if debug: print('\n Form is valid \n')
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                delivery = (request.POST['delivery_type'] == 'delivery')
                pickup = (request.POST['delivery_type'] == 'pickup')
                contact_info = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                }
                cart['details']['contact_info'] = contact_info
                if delivery:
                    if debug: print('\n Delivery!!!! \n')
                    street_one = form.cleaned_data.get('street_one')
                    street_two = form.cleaned_data.get('street_two')
                    city = form.cleaned_data.get('city')
                    state = form.cleaned_data.get('state')
                    zipcode = form.cleaned_data.get('zipcode')
                    if is_valid_form([street_one, street_two, city, state, zipcode]):
                        if debug: print('DELIVERY ADDRESS IS VALID')
                        delivery_address = {
                        'street_one': street_one,
                        'street_two': street_two,
                        'city': city,
                        'state': state,
                        'zipcode': zipcode,
                        }
                        cart['details']['delivery_address'] = delivery_address
                        cart['details']['pickup'] = False
                        if debug: print('\n Delivery done \n')
                    else:
                        context['message'] = 'Please fill in the required delivery address fields.'
                        return render (request, 'checkout.html', context=context)
                elif pickup:
                    if debug: print('\n Pickup!!! \n')
                    cart['details']['pickup'] = True
                    if debug: print('\n Pickup done \n')
            else:
                if debug: print('\n Not filled out \n')
                context['message'] = 'Please fill in the required contact information fields.'
                return render (request, 'checkout.html', context=context)
            request.session['cart'] = cart
            new_order = save_cart_as_order(cart)
            if debug: print('\nYAYAYYAYYA\n')
            context['message'] = 'Success!!! Ref code is ' + new_order.ref_code
            context['num_of_items'] = items_views.get_session_cart_size(request.session.get('cart'))

            content = send_invoice(new_order)

            return render (request, 'email_template.html', context=content)
            # request.session.pop('cart')
            # return render (request, 'confirmation.html')
    else:
        context['message'] = 'You do not have a pending order'
        return render (request, 'checkout.html', context=context)

def send_invoice(order):
    header = order.customer.first_name + ', your order has been processed!'
    item_list = order.get_item_list()
    subtotal = order.get_subtotal()
    fees = get_cart_fees(subtotal)
    total = subtotal + fees['Sales Tax'] # TODO: check this fees stuff

    print('\n' + str(item_list) + '\n')
    content = {
    'title': "Invoice from O'Whata Cookie",
    'header': header,
    'item_list': item_list,
    'num_of_items': order.get_total_quantity(),
    'fees': fees,
    'subtotal': subtotal,
    'total': total,
    'order': order,
    }
    html_content = render_to_string('email_template.html',content)

    # send_mail(
    # 'Hello from OWhata Cookie',
    # strip_tags(html_content),
    # 'sebash189@gmail.com',
    # ['bages12658@bboygarage.com'],
    # fail_silently = False,
    # html_message = html_content
    # )
    return content

def save_cart_as_order(cart):
    address = None
    if cart.get('details').get('delivery_address'):
        address = Address(
        street_one = cart.get('details').get('delivery_address').get('street_one'),
        street_two = cart.get('details').get('delivery_address').get('street_two'),
        city = cart.get('details').get('delivery_address').get('city'),
        state = cart.get('details').get('delivery_address').get('state'),
        zipcode = cart.get('details').get('delivery_address').get('zipcode'),
        )
        address.save()
    customer = Customer(
    first_name = cart.get('details').get('contact_info').get('first_name'),
    last_name = cart.get('details').get('contact_info').get('last_name'),
    email = cart.get('details').get('contact_info').get('email'),
    phone_number = cart.get('details').get('contact_info').get('phone'),
    address = address,
    )
    customer.save()
    order = Order(
    ref_code = create_ref_code(),
    customer = customer,
    ordered_date = timezone.now(),
    pickup = cart.get('details').get('pickup'),
    note = cart.get('details').get('note'),
    )
    order.save()
    id_list = cart.get('details').get('item_id_list')
    for id in id_list:
        item = Item.objects.get(id=id)
        order_item = OrderItem(
        item = item,
        quantity = cart.get(str(id)).get('quantity'),
        note = cart.get(str(id)).get('note'),
        order = order,
        )
        order_item.save()
    return order

def get_bill_dict(cart):
    bill_dict = {}
    item_list = cart.get('details').get('item_id_list')
    for id in item_list:
        order_item = cart.get(str(id))
        total_price = float(order_item.get('item').get('price')) * float(order_item.get('quantity'))
        bill_dict[order_item.get('item').get('name')] = {
        'total_price': Decimal(total_price).quantize(Decimal('0.01')),
        'quantity': order_item.get('quantity'),
        }
    return bill_dict

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

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

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
