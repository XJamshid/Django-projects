from django.contrib import admin
from .models import Category,Product,ProductImage,CommentImage,Comment,Order,OrderItem,ShippingAddress,Shipment,Customer
# Register your models here.

admin.site.register(Customer)

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(ProductImage)

admin.site.register(CommentImage)

admin.site.register(Comment)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(ShippingAddress)

admin.site.register(Shipment)
