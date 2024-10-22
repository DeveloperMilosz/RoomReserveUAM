from django.contrib import admin
from room_reserve.models.calendar import Room
from room_reserve.models.calendar import Meeting


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = ("room_number", "building_name_pl", "capacity")
    search_fields = ("room_number", "building_name_pl", "room_supervisor__username")

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):

    list_display = ("start_time", "end_time", "name_pl", "name_en", "room")
    search_fields = ("room_number", "building_name")
