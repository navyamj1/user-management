from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name', 'address', 'city', 'state', 'pincode', 'is_staff')
    
   
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('address', 'city', 'state', 'pincode', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)