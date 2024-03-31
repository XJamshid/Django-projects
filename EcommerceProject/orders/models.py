from django.db import models
from accounts.models import Customer
from products.models import Product
# Create your models here.

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    date_added=models.DateTimeField(auto_now_add=True)