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
    extra = 1
    fields = ("attribute_id", "description_pl", "description_en", "count")
    readonly_fields = ()


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
        "id",
        "name_pl",
        "name_en",
        "meeting_type",
        "start_time",
        "end_time",
        "room",
        "color",
        "event",
        "capacity",
        "is_approved",
        "is_rejected",
        "is_updated",
        "submitted_by",
    )
    search_fields = ("name_pl", "name_en", "description", "submitted_by__username", "submitted_by__email")
    list_filter = ("meeting_type", "is_approved", "is_rejected", "is_updated", "submitted_by")
    filter_horizontal = ("lecturers",)
    readonly_fields = ("submitted_by",)
    actions = ["approve_meetings", "reject_meetings"]

    # Akcja: Akceptowanie spotkań
    def approve_meetings(self, request, queryset):
        queryset.update(is_approved=True, is_rejected=False)
        self.message_user(request, "Potwierdzono wybrane spotkania.")

    # Akcja: Odrzucanie spotkań
    def reject_meetings(self, request, queryset):
        queryset.update(is_approved=False, is_rejected=True)
        self.message_user(request, "Odrzucono wybrane spotkania.")

    approve_meetings.short_description = "Potwierdź wybrane spotkania"
    reject_meetings.short_description = "Odrzuć wybrane spotkania"

    # Automatyczne ustawianie `submitted_by` przy zapisie
    def save_model(self, request, obj, form, change):
        if not obj.submitted_by:
            obj.submitted_by = request.user
        super().save_model(request, obj, form, change)


class MeetingInline(admin.TabularInline):
    model = Meeting
    extra = 1  # Number of empty rows to display
    fields = (
        "meeting_type",
        "name_pl",
        "name_en",
        "start_time",
        "end_time",
        "room",
        "capacity",
        "color",
        "event",
        "is_approved",
        "is_rejected",
        "is_updated",
        "submitted_by",
    )
    readonly_fields = ("is_updated", "submitted_by")
    show_change_link = True


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "event_type", "organizer", "start_date", "end_date")
    search_fields = ("name", "description")
    list_filter = ("event_type", "organizer")
    inlines = [MeetingInline]
