from django.db import models
# from django.contrib.auth.models import User
from decimal import *

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'ID: ' + str(self.id) + ' Name: ' + self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=8)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='/static/NoImageFound.jpg')

    def __str__(self):
        return self.name + ", Category: " + str(self.category_id)

    def get_dict_of_model(self):
        return {
        'id': self.id,
        'name': self.name,
        'price': str(self.price),
        }
