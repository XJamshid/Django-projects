from django.test import SimpleTestCase
from django.urls import reverse,resolve
from games.views import GameDetailView,LikeView, GameCreateView,GameDeleteView,GameUpdateView

class TestUrls(SimpleTestCase):
    def setUp(self):
        self.detail_url=reverse('game',args=[str(1)])
        self.create_url=reverse('game_create')
        self.update_url=reverse('game_update',args=[str(1)])
        self.delete_url=reverse('game_delete',args=[str(1)])
        self.like_url=reverse('like',args=[str(1)])
    def test_detail_url(self):
        self.assertEqual(resolve(self.detail_url).func.view_class,GameDetailView)
    def test_create_url(self):
        self.assertEqual(resolve(self.create_url).func.view_class,GameCreateView)
    def test_update_url(self):
        self.assertEqual(resolve(self.update_url).func.view_class,GameUpdateView)
    def test_delete_url(self):
        self.assertEqual(resolve(self.delete_url).func.view_class,GameDeleteView)
    def test_like_url(self):
        self.assertEqual(resolve(self.like_url).func,LikeView)

