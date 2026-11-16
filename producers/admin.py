from django.contrib import admin

from django.contrib import admin
from .models import Producer


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'region', 'phone', 'owner')
    list_filter = ('product_type', 'region')
    search_fields = ('name', 'region')
