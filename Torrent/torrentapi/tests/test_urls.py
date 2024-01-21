from rest_framework.test import APISimpleTestCase
from django.urls import reverse,resolve
from torrentapi.views import (
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

class Testurls(APISimpleTestCase):
    def setUp(self):
        self.urls=reverse('urls')
        self.categories_list=reverse('api_categories')
        self.category_detail=reverse('category',args=['Action'])
        self.games_list=reverse('games_list')
        self.game_detail=reverse('game_detail',args=['FIFA24'])
        self.game_update=reverse('game_edit',args=['FIFA24'])
        self.game_delete=reverse('game_delete', args=['FIFA24'])
        self.game_create=reverse('game_add')
        self.screenshot_add=reverse('screenshot_add')
    def test_urls(self):
        self.assertEqual(resolve(self.urls).func.view_class,UrlsAPIView)
    def test_categories_list(self):
        self.assertEqual(resolve(self.categories_list).func.view_class,CategoryListAPIView)
    def test_category_detail(self):
        self.assertEqual(resolve(self.category_detail).func.view_class,CategoryGameListAPIView)
    def test_games_list(self):
        self.assertEqual(resolve(self.games_list).func.view_class,GameListAPIView)
    def test_game_detail(self):
        self.assertEqual(resolve(self.game_detail).func.view_class,GameDetailAPIView)
    def test_game_update(self):
        self.assertEqual(resolve(self.game_update).func.view_class,GameUpdateAPIView)
    def test_game_delete(self):
        self.assertEqual(resolve(self.game_delete).func.view_class,GameDestroyAPIView)
    def test_game_create(self):
        self.assertEqual(resolve(self.game_create).func.view_class,GameCreateAPIView)
    def test_screenshot_add(self):
        self.assertEqual(resolve(self.screenshot_add).func.view_class,ScreenshotCreateAPIView)
