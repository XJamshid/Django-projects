from django.test import SimpleTestCase
from django.urls import reverse,resolve
from categories.views import CategoryDetailView,CategoryCreateView,CategoryUpdateView,CategoryDeleteView

class TestUrls(SimpleTestCase):
    def setUp(self):
        self.detail_url=reverse('category',args=[str(1)])
        self.create_url=reverse('category_create')
        self.update_url=reverse('category_update',args=[str(1)])
        self.delete_url=reverse('category_delete',args=[str(1)])
    def test_detail_url(self):
        self.assertEqual(resolve(self.detail_url).func.view_class,CategoryDetailView)
    def test_create_url(self):
        self.assertEqual(resolve(self.create_url).func.view_class,CategoryCreateView)
    def test_update_url(self):
        self.assertEqual(resolve(self.update_url).func.view_class,CategoryUpdateView)
    def test_delete_url(self):
        self.assertEqual(resolve(self.delete_url).func.view_class,CategoryDeleteView)