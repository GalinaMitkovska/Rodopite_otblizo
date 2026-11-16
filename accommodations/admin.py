from django.contrib import admin

from django.contrib import admin
from .models import Accommodation


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'accommodation_type', 'region', 'price_per_night', 'capacity', 'owner')
    list_filter = ('accommodation_type', 'region')
    search_fields = ('name', 'region')