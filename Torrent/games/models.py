from django.db import models
from embed_video.fields import EmbedVideoField
from django.urls import reverse
from django.contrib.auth import get_user_model
from categories.models import Category
# Create your models here.
class Screenshots(models.Model):
    game_name = models.CharField(max_length=100)
    screenshots=models.ImageField(upload_to='screenshots/',unique=True)
    def __str__(self):
        return self.game_name
class Game(models.Model):
    name=models.CharField(max_length=100,unique=True)
    release_date=models.DateField()
    category=models.ManyToManyField(Category)
    poster = models.ImageField(upload_to='images/',unique=True)
    trailer = EmbedVideoField()
    screenshots = models.ManyToManyField(Screenshots)
    likes=models.ManyToManyField(get_user_model())
    developer=models.CharField(max_length=200)
    platform=models.CharField(max_length=200)
    os=models.CharField(max_length=200)
    processor=models.CharField(max_length=200)
    ram=models.CharField(max_length=200)
    video_card=models.CharField(max_length=150)
    disk_space=models.CharField(max_length=50)
    file=models.FileField(upload_to='files/',unique=True)
    about=models.TextField()
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("game", args=[str(self.pk)])