from django.test import SimpleTestCase
from django.urls import reverse,resolve
from accounts.views import SignUpView
class TestUrls(SimpleTestCase):
    def setUp(self):
        self.signup_url = reverse('registration')
    def test_signup_url(self):
        self.assertEqual(resolve(self.signup_url).func.view_class,SignUpView)