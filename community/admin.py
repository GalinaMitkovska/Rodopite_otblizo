from django.contrib import admin

from django.contrib import admin
from .models import TravelStory


@admin.register(TravelStory)
class TravelStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'destination', 'created_at')
    search_fields = ('title', 'content')
