from django.contrib import admin
from .models import Category
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    model=Category
    list_display = ['id','name']
admin.site.register(Category,CategoryAdmin)