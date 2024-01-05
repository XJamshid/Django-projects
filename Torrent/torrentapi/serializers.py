
from accounts.models import CustomUser
from rest_framework import serializers
from games.models import Game,Screenshots
from categories.models import Category
from rest_framework import reverse

class CategorySerializer(serializers.ModelSerializer):
    games=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Category
        fields=[
            'name',
            'games',
        ]
    def get_games(self,obj):
        request=self.context.get('request')
        return reverse.reverse('category',kwargs={'category':obj.name},request=request)

class GameListSerializer(serializers.ModelSerializer):
    poster=serializers.SerializerMethodField(read_only=True)
    detail=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Game
        fields=[
            'detail',
            'name',
            'poster'
        ]

    def get_poster(self,obj):
        return f"http://127.0.0.1:8000{obj.poster.url}"
    def get_detail(self,obj):
        request=self.context.get('request')
        return reverse.reverse('game_detail',kwargs={'name':obj.name},request=request)

class ScreenshotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screenshots
        fields = [
            'game_name',
            'screenshots'
        ]
class GameAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Game
        fields=[
            'name',
            'category',
            'release_date',
            'poster',
            'trailer',
            'screenshots',
            'file'
        ]
class GameCategoriesSerializer(serializers.RelatedField):
    def to_representation(self,value):
        return value.name
class GameScreenshotsSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return f"http://127.0.0.1:8000{value.screenshots.url}"
class GameDetailSerializer(serializers.ModelSerializer):
    games_list = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    category=GameCategoriesSerializer(many=True,read_only=True)
    screenshots=GameScreenshotsSerializer(many=True,read_only=True)
    class Meta:
        model = Game
        fields = [
            'games_list',
            'name',
            'release_date',
            'category',
            'poster',
            'trailer',
            'screenshots',
            'file',
            'edit_url',
            'delete_url',
        ]

    def get_games_list(self, obj):
        request = self.context.get('request')
        return reverse.reverse_lazy('games_list', request=request)

    def get_edit_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('game_edit', kwargs={'name': obj.name}, request=request)

    def get_delete_url(self, obj):
        request = self.context.get('request')
        return reverse.reverse('game_delete', kwargs={'name': obj.name}, request=request)
class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'name',
            'release_date',
            'category',
            'poster',
            'trailer',
            'screenshots',
            'file',
        ]
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=[
            'username',
            'email',
            'date_of_birth',
            'password',
        ]