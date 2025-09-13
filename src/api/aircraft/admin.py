from django.contrib import admin
from .models import Manufacturer, Aircraft


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_currently_manufacturing', 'aircraft_count', 'created_at']
    list_filter = ['is_currently_manufacturing', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

    def aircraft_count(self, obj):
        return obj.aircraft.count()
    aircraft_count.short_description = 'Aircraft Count'


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = [
        'model', 
        'manufacturer', 
        'clean_stall_speed', 
        'top_speed', 
        'maneuvering_speed',
        'is_mosaic_compliant'
    ]
    list_filter = [
        'manufacturer', 
        'is_mosaic_compliant', 
        'manufacturer__is_currently_manufacturing'
    ]
    search_fields = ['model', 'manufacturer__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['manufacturer__name', 'model']
