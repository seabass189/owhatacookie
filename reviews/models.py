from django.db import models
from orders.models import Order
# from customers.models import Customer

class Review(models.Model):
    header = models.CharField(max_length=50)
    text = models.CharField(max_length=500, blank=True, null=True)
    stars = models.PositiveSmallIntegerField()
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.stars) + ' stars - Customer: '
        + str(self.customer) + ' Order: ' + str(self.order.id))
