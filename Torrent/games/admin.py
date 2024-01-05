from django.contrib import admin
from .models import Game,Screenshots
from embed_video.admin import AdminVideoMixin
# Register your models here.
class GameAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=Game
    list_display = ['id','name','release_date']
admin.site.register(Game,GameAdmin)

class ScreenshotsAdmin(admin.ModelAdmin):
    model=Screenshots
    list_display = ['id','game_name','screenshots']
admin.site.register(Screenshots,ScreenshotsAdmin)