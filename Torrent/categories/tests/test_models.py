from django.urls import reverse
from categories.models import Category
from django.test import TestCase

class TestCategoryModel(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name='Action')
    def test_category_model_entry(self):
        self.assertTrue(isinstance(self.category,Category))
    def test_str_dm(self):
        action=self.category
        self.assertEqual(str(action),action.name)
    def test_get_absolute_url_m(self):
        action=self.category
        self.assertEqual(action.get_absolute_url(),reverse('category', args=[str(action.pk)]))
