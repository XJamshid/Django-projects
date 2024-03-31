from django.urls import path
from .views import (
    CommentDetailView,
    CommentCreateView
                    )
urlpatterns=[
    path('<int:pk>/',CommentDetailView.as_view(),name='comment_detail'),
    path('create/product/<slug:slug>/',CommentCreateView.as_view(),name='comment_create')
]