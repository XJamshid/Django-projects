from django.contrib import admin
from .models import ShippingAddress,Shipment
# Register your models here.

class ShipmentAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=Shipment
    list_display = ['id','order','address','purchase_time']
admin.site.register(Shipment,ShipmentAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=ShippingAddress
    list_display = ['id','customer','region','city_or_district','neighborhood','street','post_code','home_number']
admin.site.register(ShippingAddress,ShippingAddressAdmin)