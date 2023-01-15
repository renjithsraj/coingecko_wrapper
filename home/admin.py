from django.contrib import admin
from home.models import DataStore
# Register your models here.

@admin.register(DataStore)
class DataStoreAdmin(admin.ModelAdmin):
    list_display = ['coin_id', 
        'coin_name', 'current_price', 
        'cdate', 'last_updated', 'is_active'
    ]
    date_hierarchy = 'last_updated'
    search_fields = ['coin_name']
    ordering = ['last_updated']



