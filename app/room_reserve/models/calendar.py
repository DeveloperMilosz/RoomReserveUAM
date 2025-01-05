from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
import uuid
from statistics import mean


User = get_user_model()


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


class Event(models.Model):
    LESSON_SCHEDULE = "lesson_schedule"
    GENERAL_EVENT = "event"

    EVENT_TYPE_CHOICES = [
        (LESSON_SCHEDULE, _("Lesson Schedule")),
        (GENERAL_EVENT, _("Event")),
    ]

    name = models.CharField(_("Event Name"), max_length=50, null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    organizer = models.ManyToManyField(
        User, verbose_name=_("Organizers/Lecturers"), blank=True, 
        limit_choices_to={'user_type__in': ['Lecturer', 'Organizer']}, 
        related_name="lecturer_event"
    )
    event_type = models.CharField(_("Event Type"), max_length=50, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(_("End Date"))
    color = ColorField(default="#0f2d66")
    is_approved = models.BooleanField(_("is approved"), default=False)
    is_rejected = models.BooleanField(_("is rejected"), default=False)
    logo = models.ImageField(_("Event Logo"), upload_to="event_logos/", null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)
    submitted_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, verbose_name=_("Submitted By"), null=True, blank=True
    )

    def __str__(self):
        return f"Event: {self.name}"


class RoomAttribute(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="attributes")
    attribute_id = models.CharField(_("attribute id"), max_length=100)
    description_pl = models.TextField(_("description (PL)"))
    description_en = models.TextField(_("description (EN)"))
    count = models.IntegerField(_("count"))


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
    lecturers = models.ManyToManyField(
        User, verbose_name=_("Organizers/Lecturers"), blank=True, 
        limit_choices_to={'user_type__in': ['Lecturer', 'Organizer']}, 
        related_name="lecturer_meetings"
    )
    capacity = models.IntegerField(_("meeting capacity"), null=True, blank=True)
    color = ColorField(default="#2873FF")
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name=_("Event"), related_name="meetings", null=True, blank=True
    )
    is_canceled = models.BooleanField(_("Is Canceled"), default=False)
    is_approved = models.BooleanField(_("is approved"), default=False)
    is_rejected = models.BooleanField(_("is rejected"), default=False)
    is_excel = models.BooleanField(_("is excel"), default=False)
    is_api = models.BooleanField(_("is api"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    is_updated = models.BooleanField(_("is updated"), default=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Submitted By"), 
        related_name="submitted_meetings"
    )

    def __str__(self):
        return f"{self.name_pl} ({self.start_time} - {self.end_time})"



class Notification(models.Model):
    WIADOMOSC = "message"
    POWIADOMIENIE = "notification"

    NOTIFICATION_TYPE_CHOICES = [
        (WIADOMOSC, _("message")),
        (POWIADOMIENIE, _("notification")),
    ]

    notification_type = models.CharField(
        _("Typ powiadomienia"), max_length=50, choices=NOTIFICATION_TYPE_CHOICES, null=True, blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,  # Pozwala na wartość null
        blank=True,  # Pozwala na pominięcie tego pola w formularzach
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Submitted By")
    )
    is_admin_notification = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=50,
        choices=get_user_model().USER_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Typ użytkownika, jeśli powiadomienie jest wysyłane do grupy",
    )

    def __str__(self):
        return f"Notification for {self.user.username if self.user else 'Admin'} - {self.message[:20]}"


class Group(models.Model):
    ACADEMIC_YEAR = "academic_year"
    LECTURER_GROUP = "lecturer_group"
    PERSONAL_GROUP = "personal_group"

    GROUP_TYPE_CHOICES = [
        (ACADEMIC_YEAR, _("Grupa rocznikowa")),
        (LECTURER_GROUP, _("Grupa wykładowcy")),
        (PERSONAL_GROUP, _("Grupa osobista")),
    ]

    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), null=True, blank=True)
    group_type = models.CharField(_("group type"), max_length=50, choices=GROUP_TYPE_CHOICES, default=PERSONAL_GROUP)
    admins = models.ManyToManyField(
        User, related_name="administered_groups", verbose_name=_("group admins"), blank=True
    )
    members = models.ManyToManyField(
        User, related_name="group_memberships", verbose_name=_("group members"), blank=True
    )
    meetings = models.ManyToManyField(
        "Meeting", related_name="assigned_groups", verbose_name=_("assigned meetings"), blank=True
    )
    events = models.ManyToManyField(
        "Event", related_name="assigned_groups", verbose_name=_("assigned events"), blank=True
    )
    join_requests = models.ManyToManyField(
        User, related_name="join_requests", verbose_name=_("Join Requests"), blank=True
    )
    invite_link = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_group_type_display()})"

    def add_member(self, user):
        """Add a user to the group if they're not already a member."""
        if user not in self.members.all():
            self.members.add(user)

    def remove_member(self, user):
        """Remove a user from the group if they're a member."""
        if user in self.admins.all():
            self.admins.remove(user)  # Automatyczne usunięcie z administratorów
        if user in self.members.all():
            self.members.remove(user)

    def add_admin(self, user):
        """Add a user as an admin if they're not already an admin."""
        if user not in self.admins.all():
            self.admins.add(user)
            self.add_member(user)  # Automatyczne dodanie jako członka

    def remove_admin(self, user):
        """Remove a user as an admin if they're an admin."""
        if user in self.admins.all():
            self.admins.remove(user)

    def generate_invite_link(self):
        """Generate a new unique invite link."""
        self.invite_link = uuid.uuid4()
        self.save()

    def add_join_request(self, user):
        """Add a user to the join requests."""
        if user not in self.join_requests.all():
            self.join_requests.add(user)

    def accept_join_request(self, user):
        """Accept a join request and add the user as a member."""
        if user in self.join_requests.all():
            self.join_requests.remove(user)
            self.members.add(user)

    def reject_join_request(self, user):
        """Reject a join request."""
        if user in self.join_requests.all():
            self.join_requests.remove(user)


class Status(models.Model):
    name = models.CharField(_("Status Name"), max_length=50, unique=True)
    color = ColorField(default="#CCCCCC", verbose_name=_("Status Color"))
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="statuses", verbose_name=_("Created By")
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="statuses", verbose_name=_("Group"))

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(_("Title"), max_length=100, null=True, blank=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    color = ColorField(default="#FFFFFF", verbose_name=_("Note Color"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes", verbose_name=_("Owner"))
    status = models.ForeignKey(
        Status, on_delete=models.SET_NULL, related_name="notes", null=True, blank=True, verbose_name=_("Status")
    )
    deadline = models.DateTimeField(_("Deadline"), null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="notes", verbose_name=_("Group"))

    def __str__(self):
        return self.title or f"Note {self.id}"


class RoomPlan(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name="plan")
    building_name = models.CharField(max_length=100)
    floor = models.IntegerField()
    svg_points = models.JSONField(default=list)  # Pole JSON dla punktów SVG
    plan_image = models.ImageField(upload_to="building_plans/", null=True, blank=True)

    def calculate_label_position(self):
        """Oblicza środek figury na podstawie svg_points."""
        label_positions = []
        for shape in self.svg_points:
            if shape["type"] == "polygon":
                # Rozdziel punkty wielokąta
                points = [list(map(float, point.split(","))) for point in shape["points"].split()]
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                label_positions.append({"label_x": mean(x_coords), "label_y": mean(y_coords)})
            elif shape["type"] == "rect":
                # Prostokąt - oblicz środek na podstawie x, y, width, height
                label_x = shape["x"] + (shape["width"] / 2)
                label_y = shape["y"] + (shape["height"] / 2)
                label_positions.append({"label_x": label_x, "label_y": label_y})
        return label_positions

    def __str__(self):
        return f"Plan for {self.room.room_number}"
