from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

RATING=[
    (0,0),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
]
class Customer(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.username

class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=50)
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image=models.ImageField(upload_to='product_images/')
    product_name=models.CharField(max_length=200)
    def __str__(self):
        return self.product_name

class Product(models.Model):
    name=models.CharField(max_length=200)
    brand=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField()
    price=models.FloatField()
    count=models.PositiveIntegerField(default=1)
    discount=models.BooleanField(default=False)
    discount_price=models.FloatField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ManyToManyField(ProductImage)
    slug=models.SlugField(max_length=50)
    date_added= models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Customer)
    def __str__(self):
        return self.name
    @property
    def num_orders(self):
        orders = OrderItem.objects.filter(product__pk=self.pk).filter(order__complete=True).annotate(num_orders=Sum("quantity"))
        orders = list(orders.values_list('num_orders', flat=True))
        num_orders = sum(orders)
        return num_orders

class CommentImage(models.Model):
    product_name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='comment_images/')
    def __str__(self):
        return self.product_name

class Comment(models.Model):
    body=models.TextField(null=True,blank=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    image=models.ManyToManyField(CommentImage)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    rating=models.PositiveIntegerField(choices=RATING,null=True,blank=True)
    def __str__(self):
        return self.body

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    date_added=models.DateTimeField(auto_now_add=True)

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    region=models.CharField(max_length=200)
    city_or_district=models.CharField(max_length=200)
    neighborhood=models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    post_code=models.CharField(max_length=10,null=True,blank=True)
    home_number=models.CharField(max_length=200)
class Shipment(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    purchase_time=models.DateTimeField(auto_now_add=True)
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)