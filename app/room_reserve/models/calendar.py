from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):

    room_number = models.CharField(_("room number"), max_length=30)
    building_id = models.IntegerField(_("building id"))
    building_name = models.CharField(_("building name"), max_length=50)
    capacity = models.IntegerField(_("capacity"), null=True, blank=True)
    room_supervisor = models.ForeignKey(
        "room_reserve.User",
        on_delete=models.SET_NULL,
        verbose_name=_("room supervisor"),
        blank=True,
        null=True,
    )
    # equipment = models.ManyToManyField(
    #     "AdditionalEquipment", verbose_name=_("equipment"), blank=True, null=True
    # )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    is_updated = models.BooleanField(_("is updated"), default=True)

    def __str__(self):
        return f"Room {self.room_number}"

class Meeting(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    name_pl = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
# opis, prowadzacy, liczba osob, color


    def __str__(self):
        return f"{self.name_pl} ({self.start_time} - {self.end_time})"