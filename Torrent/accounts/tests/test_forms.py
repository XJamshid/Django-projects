from django.test import TestCase
from accounts.forms import CustomUserCreationForm,CustomUserChangeForm

class TestForm(TestCase):
    def test_custom_user_creation_form(self):
        form = CustomUserCreationForm(data={
            'username': 'jamshid',
            'email': 'xudoyberdiyevjamshid8@gmail.com',
            'password1': 'jamshid1234!@#$',
            'password2': 'jamshid1234!@#$',
            'first_name': 'Jamshid',
            'last_name': 'Xudoyberdiyev',
        })
        self.assertTrue(form.is_valid())
    def test_custom_user_creation_form_no_data(self):
        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())