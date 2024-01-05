from django.urls import path,include
from .views import (
    UrlsAPIView,
    CategoryListAPIView,
    GameListAPIView,
    CategoryGameListAPIView,
    GameCreateAPIView,
    ScreenshotCreateAPIView,
    GameDetailAPIView,
    GameUpdateAPIView,
    GameDestroyAPIView,
    SignUpAPIView,
)

urlpatterns=[
    path('',UrlsAPIView.as_view(),name='urls'),
    path('categories/',CategoryListAPIView.as_view(),name='api_categories'),
    path('categories/<str:category>/',CategoryGameListAPIView.as_view(),name='category'),
    path('games_list/',GameListAPIView.as_view(),name='games_list'),
    path('games_list/<str:name>/',GameDetailAPIView.as_view(),name='game_detail'),
    path('games_list/<str:name>/edit/', GameUpdateAPIView.as_view(), name='game_edit'),
    path('games_list/<str:name>/delete/', GameDestroyAPIView.as_view(), name='game_delete'),
    path('game_add/', GameCreateAPIView.as_view(), name='game_add'),
    path('screenshot_add/', ScreenshotCreateAPIView.as_view(), name='screenshot_add'),
    #path('sign_up/',SignUpAPIView.as_view(),name='sign_up'),
]