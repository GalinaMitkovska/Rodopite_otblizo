from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser, UserProfile


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'favorite_region')
