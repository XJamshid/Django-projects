from django.urls import path,include
from .views import GameDetailView,LikeView, GameCreateView,GameDeleteView,GameUpdateView
urlpatterns = [
    path('<int:pk>/',GameDetailView.as_view(),name='game'),
    path('<int:pk>/delete/', GameDeleteView.as_view(), name='game_delete'),
    path('<int:pk>/update/', GameUpdateView.as_view(), name='game_update'),
    path('create/', GameCreateView.as_view(), name='game_create'),
    path('<int:pk>/like/',LikeView,name='like')
]