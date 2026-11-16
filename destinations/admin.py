from django.contrib import admin

from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region', 'difficulty', 'author', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('name', 'region')
