from django.urls import path
from .views import CategoryDetailView,CategoryCreateView,CategoryUpdateView,CategoryDeleteView

urlpatterns = [
    path('<int:pk>/',CategoryDetailView.as_view(),name='category'),
    path('create/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]