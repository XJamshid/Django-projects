from comments.views import CommentCreateView
from django.test import SimpleTestCase
from django.urls import reverse,resolve

class TestUrls(SimpleTestCase):
    def setUp(self):
        self.create_url=reverse('comment_create',args=[str(1)])
    def test_create_url(self):
        self.assertEqual(resolve(self.create_url).func.view_class,CommentCreateView)