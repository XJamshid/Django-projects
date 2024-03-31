
from django.urls import path
from .views import (
    Home,
    WishListView,
    SearchView
)

urlpatterns=[
    path('',Home.as_view(),name='home'),
    path('wishlist/',WishListView.as_view(),name='wishlist'),
    path('search/',SearchView.as_view(),name='search')
]
