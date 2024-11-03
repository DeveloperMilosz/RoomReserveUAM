from django.contrib import admin
from .models import Room, Lecturers, Meeting, RoomEquipment, Event

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'building_name_pl', 'building_name_en', 'capacity', 'room_supervisor', 'is_updated')
    search_fields = ('room_number', 'building_name_pl', 'building_name_en')
    list_filter = ('is_updated', 'room_supervisor')
    filter_horizontal = ('room_equipment',)

@admin.register(Lecturers)
class LecturersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'department')
    search_fields = ('first_name', 'last_name', 'email', 'department')

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name_pl', 'name_en', 'meeting_type', 'start_time', 'end_time', 'room', 'capacity', 'is_updated')
    search_fields = ('name_pl', 'name_en', 'description')
    list_filter = ('meeting_type', 'is_updated')
    filter_horizontal = ('lecturers',)

@admin.register(RoomEquipment)
class RoomEquipmentAdmin(admin.ModelAdmin):
    list_display = ('equipment_type', 'quantity', 'created_at')
    list_filter = ('equipment_type',)
    search_fields = ('equipment_type',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'organizer', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    list_filter = ('event_type', 'organizer')
    # Usunięto filter_horizontal dla `meetings`, ponieważ nie jest to ManyToManyField.
