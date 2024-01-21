from django.test import TestCase,Client
from django.urls import reverse
from comments.models import Comments
from accounts.models import CustomUser
from games.models import Game,Screenshots
from categories.models import Category
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime




#django.test.testcases.SerializeMixin ni qara




class TestViews(TestCase):
    def setUp(self):
        self.author=CustomUser.objects.create_superuser(
            username='jamshid',
            email='xudoyberdiyevjamshid8@gmail.com',
            password='jamshid1234!@#$',
            is_staff=True
        )
        self.client=Client()
        self.client.force_login(self.author)
        self.image = self.create_image()
        self.screenshot = Screenshots.objects.create(
            game_name='Test',
            screenshots=self.image
        )
        self.category = Category.objects.create(name='Action')
        self.game=self.create_game()

    def create_game(self):
        screenshot = self.screenshot
        category = self.category
        game = Game.objects.create(
            name='Test',
            release_date=datetime.date(2022, 12, 25),
            poster=self.image,
            trailer='https://www.youtube.com/watch?v=o3V-GvvzjE4',
            developer='developer',
            platform='platform',
            os='os',
            processor='processor',
            ram='ram',
            video_card='video_card',
            disk_space='disk_space',
            file=self.image,
            about='about',
        )
        game.category.add(category)
        game.screenshots.add(screenshot)
        return game

    def create_image(self):
        image_file = BytesIO()
        image = Image.new('RGB', size=(100, 100), color=(256, 0, 0))
        image.save(image_file, 'png')
        image_file.name = f'image_{datetime.datetime.now()}.png'
        image = SimpleUploadedFile(f'image_{datetime.datetime.now()}.png', image_file.getvalue(),
                                   content_type='image/png')
        return image
    def test_game_detail_view(self):
        game=self.game
        response=self.client.get(reverse('game',args=[str(game.pk)]))
        self.assertTemplateUsed(response, 'game_detail.html')
        self.assertEqual(response.status_code, 200)
        game=Game.objects.filter(pk=1)
        self.assertTrue(game.exists())
    def test_game_create_view(self):
        response=self.client.post(
            reverse('game_create'),
            data={
                'name': 'Test2',
                'release_date': datetime.date(2022, 12, 25),
                'category': self.category.pk,
                'platform': 'platform',
                'developer': 'developer',
                'os': 'os',
                'processor': 'processor',
                'ram': 'ram',
                'video_card': 'video_card',
                'disk_space': 'disk_space',
                'about': 'about',
                'poster': self.create_image(),
                'trailer': 'https://www.youtube.com/watch?v=o3V-GvvzjE4',
                'screenshots': self.screenshot.pk,
                'file': self.create_image(),
            },
        )
        game=Game.objects.get(pk=2)
        self.assertTemplateUsed("game_create.html")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(game.name, 'Test2')

    def test_update_view(self):
        response=self.client.post(
            reverse('game_update',args=[str(1)]),
            data={
                'name': 'Test2',
                'release_date': datetime.date(2023, 12, 25),
                'category': self.category.pk,
                'poster': self.create_image(),
                'trailer': 'https://www.youtube.com/watch?v=o3V-GvvzjE43',
                'screenshots': self.screenshot.pk,
                'file': self.create_image(),
            },
        )
        game=Game.objects.get(pk=1)
        self.assertEqual(game.name, 'Test2')
        self.assertTemplateUsed("game_update.html")
        self.assertEqual(response.status_code, 302)
    def test_game_delete_view(self):
        game=Game.objects.get(pk=1)
        response=self.client.post(
            reverse('game_delete',args=[str(game.pk)])
        )
        games=Game.objects.all()
        self.assertFalse(games.exists())
        self.assertTemplateUsed("game_delete.html")
        self.assertEqual(response.status_code, 302)
    def test_like_create_view(self):
        game=Game.objects.get(pk=1)
        response=self.client.post(
            reverse('like',args=[str(game.pk)]),
        )
        likes=game.likes.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(likes, 1)
