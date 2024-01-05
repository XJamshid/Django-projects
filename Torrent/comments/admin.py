from django.contrib import admin
from .models import Comments
# Register your models here.
class CommenstAdmin(admin.ModelAdmin):
    empty_value_display='_empty_'
    model=Comments
    list_display = ['id','body','game','date']
admin.site.register(Comments,CommenstAdmin)