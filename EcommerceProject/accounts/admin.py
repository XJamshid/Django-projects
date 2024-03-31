from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerCreationForm,CustomerChangeForm
from .models import Customer
class CustomerAdmin(UserAdmin):
    add_form=CustomerCreationForm
    form=CustomerChangeForm
    model=Customer
    list_display = ['username','first_name','last_name','date_of_birth','email','phone_number','is_staff']
    fieldsets = UserAdmin.fieldsets+(
        (None,{'fields':('date_of_birth','phone_number'),}),
    )
    add_fieldsets = UserAdmin.add_fieldsets+(
        (None, {'fields': ('date_of_birth','phone_number'),}),
    )

admin.site.register(Customer,CustomerAdmin)
