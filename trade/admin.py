from django.contrib import admin
from .models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'platform', 'is_active', 'created_at', 'updated_at']
    list_filter = ['platform', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['-created_at']
