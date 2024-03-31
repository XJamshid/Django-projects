from django.urls import path
from .views import (
    CheckoutView,
    ShippingAddressView,
    CheckoutReturnView,
    ShippingAddressListView,
    ShippingAddressCreateView,
    ShippingAddressDetailView,
    ShippingAddressDeleteView,
    OrderListView,
    ShipmentDetail
                    )
urlpatterns=[
    path('<int:pk>/checkout/',CheckoutView,name='checkout'),
    path('<int:pk>/shipping_address/',ShippingAddressView.as_view(),name='shipping_address_create'),
    path('<int:pk>/checkout/success/',CheckoutReturnView,name='checkout_success'),
    path('shipping_address/',ShippingAddressListView.as_view(),name='shipping_address_list'),
    path('shipping_address/create/',ShippingAddressCreateView.as_view(),name='shipping_address_create'),
    path('shipping_address/<int:pk>/',ShippingAddressDetailView.as_view(),name='shipping_address_detail'),
    path('shipping_address/<int:pk>/delete/', ShippingAddressDeleteView, name='shipping_address_delete'),
    path('shipments/',OrderListView.as_view(),name='shipments'),
    path('shipments/<int:pk>/',ShipmentDetail.as_view(),name='shipment_detail')
]