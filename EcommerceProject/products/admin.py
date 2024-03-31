from django.contrib import admin
from .models import ProductImage,Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=Product
    list_display = ['id','name','brand','price','count','discount','discount_price','category','date_added']
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)