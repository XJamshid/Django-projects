from django.db.models import Count
from django.test import TestCase,Client,RequestFactory
from django.urls import reverse
from categories.models import Category
from games.models import Game,Screenshots
from accounts.models import CustomUser
from pages.views import HomePageView,PopularGamesListView,CategoriesView,NewGamesListView,SearchView
from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

class TestViews(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name='Action')
        self.image = self.create_image()
        self.torrent = self.create_torrent()
        self.screenshot = Screenshots.objects.create(
            game_name='Test',
            screenshots=self.image
        )
        self.game1 = self.create_game(name='Test2',release_date=datetime.date(2023, 12, 25))
        self.user = CustomUser.objects.create_user(
            username='jamshid',
            email='xudoyberdiyevjamshid8@gmail.com',
            password='jamshid1234!@#$',
        )
        self.client = Client()
        self.factory = RequestFactory()
        self.client.force_login(self.user)
        self.game2=self.create_game(name='Test1',user=self.user,release_date=datetime.date(2022, 12, 25))
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
    def create_game(self,name,release_date,user=None):
        poster=self.create_image()
        file = self.create_torrent()
        screenshot=self.screenshot
        category = self.category
        game = Game.objects.create(
            name=name,
            release_date=release_date,
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
        if user is not None:
            game.likes.add(user)
        return game
    def test_home_page_view(self,filter=None):
        games = Game.objects.annotate(num_likes=Count("likes"))
        filter = filter
        if filter is not None:
            request = self.factory.get(reverse('home'),{'filter':filter})
            if filter == 'name':
                games = games.order_by(filter)
            else:
                games = games.order_by(filter).reverse()
        else:
            request = self.factory.get(reverse('home'))
            games = games.order_by('-release_date')
        response = HomePageView.as_view()(request)
        context=response.context_data['games_list']
        game=context.object_list[0]
        games = list(games)
        game1=games[0]
        self.assertTemplateUsed('home.html')
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(context),2)
        self.assertEqual(str(game),str(game1))
    def test_categories_view(self):
        request=self.factory.get(reverse('categories'))
        response=CategoriesView.as_view()(request)
        context=response.context_data['categories']
        context=list(context)
        category=context[0]
        self.assertTemplateUsed('categories.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context), 1)
        self.assertEqual(str(category), self.category.name)
    def test_popular_games_list_view(self,filter=None):
        games = Game.objects.annotate(num_likes=Count("likes"))
        filter = filter
        games_pk = games.order_by('-num_likes').values_list('pk', flat=True)[:2]
        games = games.filter(pk__in=games_pk)
        if filter is not None:
            request = self.factory.get(reverse('popular_games'),{'filter':filter})
            if filter == 'name':
                games = games.order_by(filter)
            else:
                games = games.order_by(filter).reverse()
        else:
            request = self.factory.get(reverse('popular_games'))
            games = games.order_by('-num_likes')
        response=PopularGamesListView.as_view()(request)
        context=response.context_data['games_list']
        context=context.object_list
        game = context[0]
        games = list(games)
        game1 = games[0]
        self.assertTemplateUsed('home.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context), 2)
        self.assertEqual(str(game), str(game1))
    def test_new_games_list_view(self,filter=None):
        games = Game.objects.annotate(num_likes=Count("likes"))
        games_pk = games.order_by('-release_date').values_list('pk', flat=True)[:32]
        games = games.filter(pk__in=games_pk)
        filter = filter
        if filter is not None:
            request = self.factory.get(reverse('new_games'),{'filter':filter})
            if filter == 'name':
                games = games.order_by(filter)
            else:
                games = games.order_by(filter).reverse()
        else:
            request = self.factory.get(reverse('new_games'))
            games = games.order_by('-release_date')
        response = NewGamesListView.as_view()(request)
        context = response.context_data['games_list']
        context = context.object_list
        game = context[0]
        games = list(games)
        game1 = games[0]
        self.assertTemplateUsed('home.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context), 2)
        self.assertEqual(str(game),str(game1))
    def test_search_view(self):
        request=self.factory.get(reverse('search'),{'name':'Test1'})
        response=SearchView.as_view()(request)
        context=response.context_data['games']
        context = list(context)
        game=context[0]
        self.assertTemplateUsed('search.html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(context), 1)
        self.assertEqual(str(game), 'Test1')
    def test_home_page_view_filter(self):
        self.test_home_page_view(filter='release_date')
        self.test_home_page_view(filter='num_likes')
        self.test_home_page_view(filter='name')
    def test_popular_games_list_view_filter(self):
        self.test_popular_games_list_view(filter='release_date')
        self.test_popular_games_list_view(filter='num_likes')
        self.test_popular_games_list_view(filter='name')
    def test_new_games_list_view_filter(self):
        self.test_new_games_list_view(filter='release_date')
        self.test_new_games_list_view(filter='num_likes')
        self.test_new_games_list_view(filter='name')