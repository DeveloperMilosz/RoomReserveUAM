from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
    room_number = models.CharField(_("room number"), max_length=30)
    building_id = models.IntegerField(_("building id"))
    building_name_pl = models.CharField(_("building name_pl"), max_length=50, null=True, blank=True)
    building_name_en = models.CharField(_("building name_en"), max_length=50, null=True, blank=True)
    capacity = models.IntegerField(_("capacity"), null=True, blank=True)
    room_supervisor = models.ForeignKey(
        "room_reserve.User", on_delete=models.SET_NULL, verbose_name=_("room supervisor"), blank=True, null=True
    )
    room_equipment = models.ManyToManyField("RoomEquipment", verbose_name=_("equipment"), blank=True)
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
        (MEETING, _("meeting")),
        (CLASS_GROUP, _("classgroup")),
    ]

    meeting_type = models.CharField(_("meeting type"), max_length=50, choices=MEETING_TYPE_CHOICES, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name_pl = models.CharField(_("name pl"), max_length=80, null=True, blank=True)
    name_en = models.CharField(_("name en"), max_length=255, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=_("room number"), blank=True, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    lecturers = models.ManyToManyField(Lecturers, verbose_name=_("Lecturers"), blank=True)
    capacity = models.IntegerField(_("meeting capacity"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    is_updated = models.BooleanField(_("is updated"), default=True)

    def __str__(self):
        return f"{self.name_pl} ({self.start_time} - {self.end_time})"


class EquipmentType(models.TextChoices):
    PROJECTOR = "projector", _("Projector")
    SINK = "sink", _("Sink")
    WHITEBOARD = "whiteboard", _("Whiteboard")
    INTERACTIVE_WHITEBOARD = "interactive_whiteboard", _("Interactive Whiteboard")
    COMPUTER = "computer", _("Computer")
    WIRELESS_MICROPHONE = "wireless_microphone", _("Wireless Microphone")
    VISUALIZER = "visualizer", _("Visualizer")
    INTERNET_ACCESS = "internet_access", _("Internet Access")
    AUDITORY_DESKS = "auditory_desks", _("Auditory Desks")
    SEATING_PLACES = "seating_places", _("Seating Places")
    FLIPCHART = "flipchart", _("Flipchart")
    SHOWER = "shower", _("Shower")
    ACID_RESISTANT_TABLES = "acid_resistant_tables", _("Acid-Resistant Tables")
    SERVER = "server", _("Server")
    NETWORK_DEVICES = "network_devices", _("Network Devices")


class RoomEquipment(models.Model):
    equipment_type = models.CharField(_("Equipment Type"), max_length=50, choices=EquipmentType.choices)
    quantity = models.IntegerField(_("Quantity"), default=1)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["equipment_type"], name="unique_equipment_type")]
        verbose_name = _("Room Equipment")
        verbose_name_plural = _("Room Equipment")

    def __str__(self):
        return f"{self.get_equipment_type_display()} (Quantity: {self.quantity})"


class Event(models.Model):
    LESSON_SCHEDULE = "lesson_schedule"  # text choices
    GENERAL_EVENT = "event"

    EVENT_TYPE_CHOICES = [
        (LESSON_SCHEDULE, _("Lesson Schedule")),
        (GENERAL_EVENT, _("Event")),
    ]

    name = models.CharField(_("Event Name"), max_length=50, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    meetings = models.ManyToManyField(Meeting, verbose_name=_("Meetings"), blank=True)
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
