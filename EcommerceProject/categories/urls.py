from django.urls import path
from .views import (
    CategoryDetailView,
    CategoryDeleteView,
    CategoryCreateView,
    CategoryUpdateView
                        )
urlpatterns=[
    path('<slug:slug>/',CategoryDetailView.as_view(),name='category'),
    path('<slug:slug>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),

]