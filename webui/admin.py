from django.contrib import admin
from .models import Area, Parameter, Station, Measurement


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['name', 'city']}),
    ]
    model = Area
    list_display = ('name', 'city')
    save_on_top = False


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['name', 'url', 'street', 'area', 'parser', 'added']}),
    ]
    model = Station
    list_display = ('name', 'street', 'area', 'added')
    save_on_top = False


@admin.register(Parameter)
class ParamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['name', 'description', 'norm']}),
    ]
    model = Parameter
    list_display = ('name', 'norm')
    save_on_top = False


@admin.register(Measurement)
class MeasureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,   {'fields': ['station', 'type', 'value', 'date']}),
    ]
    model = Measurement
    list_display = ('date', 'value', 'type', 'station')
    save_on_top = False
