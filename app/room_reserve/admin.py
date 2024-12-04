from django.contrib import admin
from .models import Room, Lecturers, Meeting, RoomAttribute, Event


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "room_number",
        "building_id",
        "building_name_pl",
        "building_name_en",
        "capacity",
        "room_supervisor",
    )
    search_fields = (
        "room_number",
        "building_name_pl",
        "building_name_en",
        "room_supervisor__username",
    )
    list_filter = ("building_name_pl", "building_name_en", "capacity")
    ordering = ("room_number", "building_id")
    inlines = []  # Inline RoomAttributes added below


# RoomAttributeInline for RoomAdmin
class RoomAttributeInline(admin.TabularInline):
    model = RoomAttribute
    extra = 1  # Show one empty row for adding new attributes
    fields = ("attribute_id", "description_pl", "description_en", "count")
    readonly_fields = ()  # Optional: Set fields to read-only if necessary


# Add RoomAttributeInline to RoomAdmin
RoomAdmin.inlines.append(RoomAttributeInline)


@admin.register(RoomAttribute)
class RoomAttributeAdmin(admin.ModelAdmin):
    list_display = ("room", "attribute_id", "description_pl", "description_en", "count")
    search_fields = ("attribute_id", "description_pl", "description_en", "room__room_number")
    list_filter = ("attribute_id",)
    ordering = ("room", "attribute_id")


@admin.register(Lecturers)
class LecturersAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "department")
    search_fields = ("first_name", "last_name", "email", "department")


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        "name_pl",
        "name_en",
        "meeting_type",
        "start_time",
        "end_time",
        "room",
        "capacity",
        "is_approved",  # Added for approval workflow
        "is_updated",
    )
    search_fields = ("name_pl", "name_en", "description")
    list_filter = ("meeting_type", "is_approved", "is_updated")  # Filter by approval status
    filter_horizontal = ("lecturers",)
    actions = ["approve_meetings", "reject_meetings"]

    # Add approval actions for meetings
    def approve_meetings(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected meetings have been approved.")

    def reject_meetings(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected meetings have been rejected.")

    approve_meetings.short_description = "Approve selected meetings"
    reject_meetings.short_description = "Reject selected meetings"


# MeetingInline for EventAdmin
class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1  # Number of empty rows to display
    fields = ("meeting_type", "name_pl", "name_en", "start_time", "end_time", "room", "capacity", "color", "is_approved", "is_updated")
    readonly_fields = ("is_updated",)  # Optional: Make specific fields read-only
    show_change_link = True  # Enable navigation to edit meetings


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_type", "organizer", "start_date", "end_date")
    search_fields = ("name", "description")
    list_filter = ("event_type", "organizer")
    inlines = [MeetingInline]  # Add MeetingInline to EventAdmin
