from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.urls import reverse
from accounts.views import  SignUpView
from accounts.models import CustomUser
class TestSignUpView(TestCase):
    def setUp(self):
        self.client=Client()
    def test_sign_up_view(self):
        response=self.client.post(reverse('registration'),
                                  data={
                                      'username':'jamshid',
                                      'email':'xudoyberdiyevjamshid8@gmail.com',
                                      'password1':'jamshid1234!@#$',
                                      'password2': 'jamshid1234!@#$',
                                      'first_name':'Jamshid',
                                      'last_name':'Xudoyberdiyev',
                                  }
                                  )
        user=CustomUser.objects.get(pk=1)
        self.assertEqual(response.status_code,302)
        self.assertEqual(user.username, 'jamshid')