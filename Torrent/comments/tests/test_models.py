from django.urls import reverse
from comments.models import Comments
from accounts.models import CustomUser
from games.models import Game,Screenshots
from categories.models import Category
from django.test import TestCase
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class TestCategoryModel(TestCase):
    def setUp(self):
        self.author=CustomUser.objects.create_user(
            username='jamshid',
            email='xudoyberdiyevjamshid8@gmail.com',
            password='jamshid1234!@#$',
        )
        self.game=self.create_game()
        self.comment=Comments.objects.create(
            author=self.author,
            body='body',
            date=datetime.date(2022, 12, 25),
            game=self.game
        )
    def create_game(self):
        file_obj = BytesIO()
        image_file = Image.new('RGB', size=(100, 100), color=(256, 0, 0))
        image_file.save(file_obj, 'png')
        torrent_file = StringIO()
        torrent_file.write('Test torrent file')
        image = SimpleUploadedFile('image.png', file_obj.read(), content_type='image/png')
        torrent = SimpleUploadedFile('torrent_file.torrent', torrent_file.read(), content_type='file/torrent')
        screenshot = Screenshots.objects.create(
            game_name='Test',
            screenshots=image
        )
        category = Category.objects.create(name='Action')
        game = Game.objects.create(
            name='Test',
            release_date=datetime.date(2022, 12, 25),
            poster=image,
            trailer='https://www.youtube.com/watch?v=o3V-GvvzjE4',
            developer='developer',
            platform='platform',
            os='os',
            processor='processor',
            ram='ram',
            video_card='video_card',
            disk_space='disk_space',
            file=torrent,
            about='about',
        )
        game.category.add(category)
        game.screenshots.add(screenshot)
        return game
    def test_comment_model_entry(self):
        comment=Comments.objects.get(pk=1)
        self.assertEqual(comment.pk,1)
        self.assertTrue(isinstance(self.comment,Comments))