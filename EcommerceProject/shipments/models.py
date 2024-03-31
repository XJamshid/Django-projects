from django.db import models
from accounts.models import Customer
from orders.models import Order
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    phone = PhoneNumberField(null=True,blank=True)
    region=models.CharField(max_length=200)
    city_or_district=models.CharField(max_length=200)
    neighborhood=models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    post_code=models.CharField(max_length=10,null=True,blank=True)
    home_number=models.CharField(max_length=200)
    is_default=models.BooleanField(default=False)
class Shipment(models.Model):
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    purchase_time=models.DateTimeField(auto_now_add=True)