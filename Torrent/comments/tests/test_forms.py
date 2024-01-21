from django.test import TestCase
from comments.forms import CommentAddForm

class TestForm(TestCase):
    def test_comment_add_form(self):
        form = CommentAddForm(
            data={
                'body': 'Body'
            }
        )
        self.assertTrue(form.is_valid())
    def test_comment_add_form_no_data(self):
        form = CommentAddForm(data={})
        self.assertFalse(form.is_valid())