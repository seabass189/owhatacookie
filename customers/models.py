from django.db import models

class Address(models.Model):
    street_one = models.CharField(max_length=50, default='')
    street_two = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=15, default='')
    zipcode = models.CharField(max_length=9, default='')

    def __str__(self):
        return self.street_one + ' ' + self.city + ' ' + self.state + ' ' + self.zipcode

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, default='')
    # stripeid = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
