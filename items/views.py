from django.shortcuts import render
from .models import Category, Item

def home(request):
    return render (request, 'items/home.html')

def items_list(request):
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
    }
    return render (request, 'items/items_list.html', context=context)
