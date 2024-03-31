from django.contrib import admin
from .models import Comment,CommentImage
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=Comment
    list_display = ['id','body','customer','product','date','rating']
admin.site.register(Comment,CommentAdmin)
admin.site.register(CommentImage)