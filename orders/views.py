from django.shortcuts import render
from items import views as items_views

def session_checkout(request):
    context = {
    'num_of_items': items_views.get_session_cart_size(request.session.get('cart')),
    }
    return render (request, 'checkout.html', context=context)
