from django.test import TestCase
from games.forms import GameCreateForm
from games.models import Screenshots,Game
from categories.models import Category
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime


class TestForm(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Action')
        self.image = self.create_image()
        self.torrent = self.create_torrent()
        self.screenshot = Screenshots.objects.create(
            game_name='Test',
            screenshots=self.image
        )
    def create_image(self):
        file_obj = BytesIO()
        image_file = Image.new('RGB', size=(100, 100), color=(256, 0, 0))
        image_file.save(file_obj, 'png')
        image = SimpleUploadedFile('image.png', file_obj.read(), content_type='image/png')
        return image
    def create_torrent(self):
        torrent_file = StringIO()
        torrent_file.write('Test torrent file')
        torrent = SimpleUploadedFile('torrent_file.torrent', torrent_file.read(), content_type='file/torrent')
        return torrent
    def test_comment_add_form(self):
        file=self.create_torrent()
        poster=self.create_image()
        form = GameCreateForm(
            data={
                'name': 'Test',
                'release_date': datetime.date(2022, 12, 25),
                'category': [self.category,],
                'platform': 'platform',
                'developer': 'developer',
                'os': 'os',
                'processor': 'processor',
                'ram': 'ram',
                'video_card': 'video_card',
                'disk_space': 'disk_space',
                'about': 'about',
                'poster': poster,
                'trailer': 'https://www.youtube.com/watch?v=o3V-GvvzjE4',
                'screenshots': [self.screenshot,],
                'file': file,

            }
        )
        self.assertFalse(form.is_valid())
    def test_comment_add_form_no_data(self):
        form = GameCreateForm(data={})
        self.assertFalse(form.is_valid())