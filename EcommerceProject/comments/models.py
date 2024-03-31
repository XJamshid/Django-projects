from django.db import models
from accounts.models import Customer
from products.models import Product
# Create your models here.
RATING=[
    (0,0),
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
]
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