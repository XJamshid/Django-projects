from django.urls import path
from .views import HomePageView,CategoriesView,PopularGamesListView,NewGamesListView, SearchView
urlpatterns=[
    path('',HomePageView.as_view(),name='home'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('popular_games/',PopularGamesListView.as_view(),name='popular_games'),
    path('new_games/', NewGamesListView.as_view(), name='new_games'),
    path('search/', SearchView.as_view(), name='search'),
]