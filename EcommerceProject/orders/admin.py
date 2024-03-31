from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=Order
    list_display = ['id','customer','date_ordered','complete']
admin.site.register(Order,OrderAdmin)
class OrderItemAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=OrderItem
    list_display = ['id','product','order','quantity','date_added']
admin.site.register(OrderItem,OrderItemAdmin)
