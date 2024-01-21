from django.urls import reverse,resolve
from pages.views import HomePageView,PopularGamesListView,CategoriesView,NewGamesListView,SearchView
from django.test import SimpleTestCase

class TestUrls(SimpleTestCase):
    def setUp(self):
        self.home_url=reverse('home')
        self.categories_url=reverse('categories')
        self.popular_games_url=reverse('popular_games')
        self.new_games_url=reverse('new_games')
        self.search_url=reverse('search')
    def test_home_url(self):
        self.assertEqual(resolve(self.home_url).func.view_class,HomePageView)
    def test_categories_url(self):
        self.assertEqual(resolve(self.categories_url).func.view_class,CategoriesView)
    def test_popular_games_url(self):
        self.assertEqual(resolve(self.popular_games_url).func.view_class,PopularGamesListView)
    def test_new_games_url(self):
        self.assertEqual(resolve(self.new_games_url).func.view_class,NewGamesListView)
    def test_search_url(self):
        self.assertEqual(resolve(self.search_url).func.view_class,SearchView)