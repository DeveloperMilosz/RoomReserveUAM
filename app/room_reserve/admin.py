from django.contrib import admin
from room_reserve.models import Room, Lecturers, Meeting, RoomAttribute, Event, User, Notification
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "first_name", "last_name", "user_type", "is_active", "is_staff")
    list_filter = ("user_type", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "department", "username")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("User Type"), {"fields": ("user_type",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type", "is_active", "is_staff"),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email",)


# Register the custom user admin
admin.site.register(User, CustomUserAdmin)


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
    list_display = ("name", "event_type", "organizer", "start_date", "end_date", "is_approved")  # Added is_approved
    search_fields = ("name", "description")
    list_filter = ("event_type", "organizer", "is_approved")  # Filter by approval status
    inlines = [MeetingInline]
    actions = ["approve_events", "reject_events"]

    def approve_events(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected events have been approved.")

    def reject_events(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected events have been rejected.")

    approve_events.short_description = "Approve selected events"
    reject_events.short_description = "Reject selected events"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message_preview", "is_read", "submitted_by", "created_at")
    list_filter = ("is_read", "created_at", "submitted_by")
    search_fields = ("user__username", "message", "submitted_by__username", "submitted_by__email")
    ordering = ("-created_at",)
    readonly_fields = ("submitted_by",)

    def message_preview(self, obj):
        """Return a short preview of the notification message."""
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")

    message_preview.short_description = "Message Preview"

    # Automatyczne ustawianie `submitted_by` przy zapisie
    def save_model(self, request, obj, form, change):
        if not obj.submitted_by:
            obj.submitted_by = request.user
        super().save_model(request, obj, form, change)
