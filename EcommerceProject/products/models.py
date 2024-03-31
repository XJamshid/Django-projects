from django.db import models
from accounts.models import Customer
from categories.models import Category
# Create your models here.

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
    count=models.PositiveIntegerField()
    discount=models.BooleanField(default=False)
    discount_price=models.FloatField(default=0)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ManyToManyField(ProductImage)
    slug=models.SlugField(max_length=50)
    date_added= models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Customer,null=True,blank=True)
    def __str__(self):
        return self.name