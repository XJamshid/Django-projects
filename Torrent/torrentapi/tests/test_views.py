from games.models import Game,Screenshots
import json
from categories.models import Category
from accounts.models import CustomUser
from rest_framework.test import APITestCase,APIClient,APIRequestFactory
from django.urls import reverse
from rest_framework import status
from torrentapi.views import (
    UrlsAPIView,
    CategoryListAPIView,
    GameListAPIView,
    CategoryGameListAPIView,
    GameCreateAPIView,
    ScreenshotCreateAPIView,
    GameDetailAPIView,
    GameUpdateAPIView,
    GameDestroyAPIView,
    SignUpAPIView,
)
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class TestViews(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_superuser(
            username='jamshid',
            email='xudoyberdiyevjamshid8@gmail.com',
            password='jamshid1234!@#$',
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.image = self.create_image()
        self.screenshot = Screenshots.objects.create(
            game_name='Test',
            screenshots=self.image
        )
        self.category = Category.objects.create(name='Action')
        self.game = self.create_game()

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
        image = SimpleUploadedFile(f'image_{datetime.datetime.now()}.png', image_file.getvalue(), content_type='image/png')
        return image
    def test_urls_api_view(self):
        response=self.client.get(reverse('urls'))
        self.assertEqual(response.data,{'urls':[f"http://testserver{reverse('api_categories')}",f"http://testserver{reverse('games_list')}"]})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_category_ist_api_view_no_data(self):
        response=self.client.get(reverse('api_categories'))
        response_data=json.loads(response.content)#response.data ni yuklab oldik
        self.assertEqual(response_data['results'],[{'name': 'Action','games':f"http://testserver{reverse('category',args=['Action'])}"}])
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    def test_category_ist_api_view(self):
        data={
            'name':'Horror'
        }
        response=self.client.post(reverse('api_categories'),data=data,format='json')
        category=Category.objects.get(pk=2)
        self.assertEqual(category.name,'Horror')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    def test_category_game_list_api_view(self):
        response=self.client.get(reverse('category',args=['Action']))
        response_data=json.loads(response.content)[0]
        #View da list metodidan foydalanilgani uchun response.content list bo'ladi
        #listning bittagina dict dan iborat bo'ladi
        self.assertEqual(response_data['name'],'Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_games_list_api_view(self):
        response=self.client.get(reverse('games_list'))
        response_data=json.loads(response.content)
        self.assertEqual(response_data['all_games'][0]['name'],'Test')
        self.assertEqual(response_data['add_game'],f"http://testserver{reverse('game_add')}")
        self.assertEqual(response_data['add_screenshot'],f"http://testserver{reverse('screenshot_add')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_game_detail_view(self):
        response=self.client.get(reverse('game_detail',args=['Test']))
        response_data=json.loads(response.content)
        self.assertEqual(response_data['name'],'Test')
        self.assertEqual(response_data['games_list'],f"http://testserver{reverse('games_list')}")
        self.assertEqual(response_data['category'],['Action'])
        self.assertEqual(response_data['edit_url'],f"http://testserver{reverse('game_edit',args=['Test'])}")
        self.assertEqual(response_data['delete_url'],f"http://testserver{reverse('game_delete',args=['Test'])}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_screenshot_create_api_view(self):
        data={
            'game_name':'Test',
            'screenshots':self.create_image(),
        }
        response=self.client.post(reverse('screenshot_add'),data=data,format='multipart')
        screenshot=Screenshots.objects.get(pk=2)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(screenshot.game_name,'Test')
    def test_game_create_api_view(self):
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
        }
        response=self.client.post(reverse('game_add'),data=data,format='multipart')
        game=Game.objects.get(pk=2)
        self.assertEqual(game.name,'Test2')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    def test_game_update_view(self):
        data={
            'name':'Test2',
            'release_date':datetime.date(2023, 12, 25),
            'category':self.category.pk,
            'poster':self.create_image(),
            'trailer':'https://www.youtube.com/watch?v=o3V-GvvzjE43',
            'screenshots':self.screenshot.pk,
            'file':self.create_image(),
            'platform': 'platform',
            'developer': 'developer',
            'os': 'os',
            'processor': 'processor',
            'ram': 'ram',
            'video_card': 'video_card',
            'disk_space': 'disk_space',
            'about': 'about',
        }
        response=self.client.put(reverse('game_edit',args=['Test']),data=data,format='multipart')
        game=Game.objects.get(pk=1)
        self.assertEqual(game.name, 'Test2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_game_delete_api_view(self):
        response = self.client.delete(reverse('game_delete', args=['Test']))
        game=Game.objects.all()
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertFalse(game.exists())
