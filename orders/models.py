from django.db import models
from items.models import Item
from customers.models import Customer

class Order(models.Model):
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, blank=True, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    pickup = models.BooleanField(default=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    # CAN ONLY IMPLEMENT ONCE CUSTOMERS CAN CREATE USERS
    # review = models.ForeignKey(Review,on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.ref_code + " - " + str(self.customer) + " ORDERED: " + str(self.ordered_date)

    def get_subtotal(self):
        total = 0
        order_items = list(OrderItem.objects.filter(order=self))
        for order_item in order_items:
            # order_item = order_orderitem.order_item
            total += order_item.get_total_item_price()
        return total

    def get_total_quantity(self):
        total = 0
        order_items = list(OrderItem.objects.filter(order=self))
        for order_item in order_items:
            # order_item = order_orderitem.order_item
            total += order_item.quantity
        return total

    def get_order_list(self):
        order_list = dict()
        order_items = list(OrderItem.objects.filter(order=self))
        for order_item in order_items:
            order_list[order_item.item.name] = {
            'total_price': order_item.get_total_item_price(),
            'quantity': order_item.quantity,
            }
        return order_list

    def get_item_list(self):
        item_list = []
        order_items = list(OrderItem.objects.filter(order=self))
        for order_item in order_items:
            item_list.append({
            'name': order_item.item.name,
            'total_price': order_item.get_total_item_price(),
            'quantity': order_item.quantity,
            'note': order_item.note,
            })
        return item_list

    def get_sales_tax(self):
        return Decimal(float(self.get_subtotal()) * 0.09).quantize(Decimal('0.01'))

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    note = models.CharField(max_length=500, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item) + ": " + str(self.quantity)

    def get_total_item_price(self):
        return self.quantity * self.item.price
