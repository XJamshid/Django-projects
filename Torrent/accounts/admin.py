from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser
class CustomUserAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomUserChangeForm
    model=CustomUser
    list_display = ['username','first_name','last_name','date_of_birth','email','is_staff']
    fieldsets = UserAdmin.fieldsets+(
        (None,{'fields':('date_of_birth',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets+(
        (None, {'fields': ('date_of_birth',)}),
    )

admin.site.register(CustomUser,CustomUserAdmin)