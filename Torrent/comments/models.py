from django.db import models
from django.contrib.auth import get_user_model
from games.models import Game
# Create your models here.
class Comments(models.Model):
    author=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    game=models.ForeignKey(Game,on_delete=models.CASCADE)