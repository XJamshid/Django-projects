from django.urls import path
from .views import CommentCreateView

urlpatterns=[
    path('game/<int:pk>/create/',CommentCreateView.as_view(),name='comment_create'),
]