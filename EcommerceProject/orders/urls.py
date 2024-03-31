from django.urls import path
from .views import (
    CartDetailView,
    OrderItemCreateView,
    OrderItemUpdateView,
    OrderItemDeleteView
                       )
urlpatterns=[
    path('',CartDetailView.as_view(),name='cart'),
    path('add_to_cart/<slug:slug>/',OrderItemCreateView.as_view(),name='add_to_cart'),
    path('update/<int:pk>/',OrderItemUpdateView.as_view(),name='update_cart'),
    path('delete/<int:pk>/',OrderItemDeleteView,name='delete_orderitem'),
]