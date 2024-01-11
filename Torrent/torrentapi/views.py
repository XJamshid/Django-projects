from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics , reverse , permissions , authentication
from games.models import Game,Screenshots
from categories.models import Category
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CategorySerializer,
    GameListSerializer,
    GameAddSerializer,
    ScreenshotCreateSerializer,
    GameDetailSerializer,
    GameUpdateSerializer,
    SignUpSerializer,
)
from .permissions import IsAdminOrReadOnly
from .paginations import StandardResultsSetPagination
from accounts.models import CustomUser
# Create your views here.

class UrlsAPIView(APIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.BasicAuthentication]
    def get(self,request,*args,**kwargs):
        categories=reverse.reverse('api_categories',request=request)
        all_games=reverse.reverse('games_list',request=request)
        #sign_up=reverse.reverse('sign_up',request=request)
        return Response({'urls':[categories,all_games]})

class CategoryListAPIView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields=['name']
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class =StandardResultsSetPagination
class CategoryGameListAPIView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = GameListSerializer
    queryset = Game.objects.all()
    pagination_class = StandardResultsSetPagination
    def list(self, request, *args, **kwargs):
        category = kwargs.get('category')
        queryset=self.get_queryset()
        print(type(queryset))
        games = queryset.filter(category__name__icontains=category)
        serializer = self.get_serializer(games, many=True)
        return Response(serializer.data)
class GameListAPIView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = GameListSerializer
    queryset = Game.objects.all()
    pagination_class = StandardResultsSetPagination
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        add_game = reverse.reverse('game_add', request=request)
        add_screenshot = reverse.reverse('screenshot_add', request=request)
        return Response({'all_games': serializer.data, 'add_game': add_game, 'add_screenshot': add_screenshot})
class GameCreateAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    serializer_class = GameAddSerializer
    queryset = Game.objects.all()
class ScreenshotCreateAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    serializer_class = ScreenshotCreateSerializer
    queryset = Screenshots.objects.all()
class GameDetailAPIView(generics.RetrieveAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = GameDetailSerializer
    queryset = Game.objects.all()
    lookup_field = 'name'
class GameUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    queryset=Game.objects.all()
    serializer_class = GameUpdateSerializer
    lookup_field = 'name'

class GameDestroyAPIView(generics.DestroyAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAdminUser]
    queryset=Game.objects.all()
    serializer_class = GameDetailSerializer
    lookup_field='name'

class SignUpAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    serializer_class = SignUpSerializer
    queryset = CustomUser.objects.all()