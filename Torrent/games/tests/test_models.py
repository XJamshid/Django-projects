from django.urls import reverse
from games.models import Screenshots,Game
from accounts.models import CustomUser
from django.test import TestCase
from categories.models import Category
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class TestModel(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name='Action')
        self.image=self.create_image()
        self.torrent=self.create_torrent()
        self.screenshot=Screenshots.objects.create(
            game_name='Test',
            screenshots=self.image
        )
        self.game=self.create_game()
    def create_game(self):
        poster=self.create_image()
        file = self.create_torrent()
        screenshot=self.screenshot
        category = self.category
        game = Game.objects.create(
            name='Test',
            release_date=datetime.date(2022, 12, 25),
            poster=poster,
            trailer='https://www.youtube.com/watch?v=o3V-GvvzjE4',
            developer='developer',
            platform='platform',
            os='os',
            processor='processor',
            ram='ram',
            video_card='video_card',
            disk_space='disk_space',
            file=file,
            about='about',
        )
        game.category.add(category)
        game.screenshots.add(screenshot)
        return game
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
    def test_category_model_entry(self):
        self.assertTrue(isinstance(self.game,Game))
    def test_str_dm(self):
        game=self.game
        self.assertEqual(str(game),game.name)
    def test_get_absolute_url_m(self):
        game=self.game
        self.assertEqual(game.get_absolute_url(),reverse("game", args=[str(game.pk)]))