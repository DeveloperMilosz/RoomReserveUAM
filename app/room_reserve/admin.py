from django.contrib import admin
from room_reserve.models.calendar import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = ("room_number", "building_name", "capacity", "room_supervisor")
    search_fields = ("room_number", "building_name", "room_supervisor__username")
