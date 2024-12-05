from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField


class Room(models.Model):
    room_number = models.CharField(_("room number"), max_length=30)
    building_id = models.IntegerField(_("building id"))
    building_name_pl = models.CharField(_("building name_pl"), max_length=50, null=True, blank=True)
    building_name_en = models.CharField(_("building name_en"), max_length=50, null=True, blank=True)
    capacity = models.IntegerField(_("capacity"), null=True, blank=True)
    room_supervisor = models.ForeignKey(
        "room_reserve.User", on_delete=models.SET_NULL, verbose_name=_("room supervisor"), blank=True, null=True
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    is_updated = models.BooleanField(_("is updated"), default=True)

    def __str__(self):
        return f"Room {self.room_number}"


class Lecturers(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=50, unique=True, null=True, blank=True)
    department = models.CharField(_("Department"), max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Meeting(models.Model):
    MEETING = "meeting"
    CLASS_GROUP = "classgroup"

    MEETING_TYPE_CHOICES = [
        (MEETING, _("Spotkanie")),
        (CLASS_GROUP, _("Grupa zajęciowa")),
    ]

    meeting_type = models.CharField(
        _("Typ spotkania"), max_length=50, choices=MEETING_TYPE_CHOICES, null=True, blank=True
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name_pl = models.CharField(_("name pl"), max_length=80, null=True, blank=True)
    name_en = models.CharField(_("name en"), max_length=255, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("room number"), blank=True, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    lecturers = models.ManyToManyField(Lecturers, verbose_name=_("Lecturers"), blank=True)
    capacity = models.IntegerField(_("meeting capacity"), null=True, blank=True)
    color = ColorField(default="#2873FF")
    event = models.ForeignKey(
        "Event", verbose_name=_("Event"), on_delete=models.CASCADE, related_name="meetings", null=True, blank=True
    )
    is_approved = models.BooleanField(_("is approved"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    is_updated = models.BooleanField(_("is updated"), default=True)

    def __str__(self):
        return f"{self.name_pl} ({self.start_time} - {self.end_time})"


class RoomAttribute(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="attributes")
    attribute_id = models.CharField(_("attribute id"), max_length=100)
    description_pl = models.TextField(_("description (PL)"))
    description_en = models.TextField(_("description (EN)"))
    count = models.IntegerField(_("count"))


class Event(models.Model):
    LESSON_SCHEDULE = "lesson_schedule"
    GENERAL_EVENT = "event"

    EVENT_TYPE_CHOICES = [
        (LESSON_SCHEDULE, _("Lesson Schedule")),
        (GENERAL_EVENT, _("Event")),
    ]

    name = models.CharField(_("Event Name"), max_length=50, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    organizer = models.ForeignKey(
        Lecturers, on_delete=models.SET_NULL, verbose_name=_("Organizer"), null=True, blank=True
    )
    event_type = models.CharField(_("Event Type"), max_length=50, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    def __str__(self):
        return f"Event: {self.name}"
