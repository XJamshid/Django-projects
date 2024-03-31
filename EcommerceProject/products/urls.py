from django.urls import path
from .views import (
    ProductDetailView,
    LikeView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView
                    )
urlpatterns=[
    path('<slug:slug>/',ProductDetailView.as_view(),name='product'),
    path('<slug:slug>/like/',LikeView.as_view(),name='like'),
    path('product/add/',ProductCreateView.as_view(),name='product_create'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<slug:slug>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]