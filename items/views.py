from django.shortcuts import render
from .models import Category, Item

def home(request):
    return render (request, 'items/home.html')
