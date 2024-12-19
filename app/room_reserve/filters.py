from django_filters import rest_framework as filters
from room_reserve.models import Meeting, Event, Room, Group
from django.db.models import Q


class MeetingFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start_time", lookup_expr="date", label="Data spotkania")
    start_time = filters.TimeFilter(field_name="start_time", lookup_expr="time", label="Godzina rozpoczęcia")
    name = filters.CharFilter(field_name="name_pl", lookup_expr="icontains", label="Nazwa spotkania")
    lecturer = filters.CharFilter(field_name="lecturers__first_name", lookup_expr="icontains", label="Prowadzący")
    room = filters.CharFilter(field_name="room__room_number", lookup_expr="icontains", label="Sala")
    meeting_type = filters.ChoiceFilter(choices=Meeting.MEETING_TYPE_CHOICES, label="Typ spotkania")
    capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte", label="Minimalna liczba osób")
    event = filters.ModelChoiceFilter(
        queryset=Event.objects.all(), field_name="event", label="Wydarzenie", empty_label="-- Wybierz --"
    )

    class Meta:
        model = Meeting
        fields = ["start_date", "start_time", "name", "lecturer", "room", "meeting_type", "capacity", "event"]


class EventFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start_date", lookup_expr="date", label="Data wydarzenia")
    start_time = filters.TimeFilter(field_name="start_date", lookup_expr="time", label="Godzina rozpoczęcia")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="Nazwa wydarzenia")
    organizer = filters.CharFilter(field_name="organizer__first_name", lookup_expr="icontains", label="Organizator")

    class Meta:
        model = Event
        fields = ["start_date", "start_time", "name", "organizer"]


class RoomFilter(filters.FilterSet):
    room_number = filters.CharFilter(field_name="room_number", lookup_expr="icontains", label="Nazwa sali")
    attribute = filters.CharFilter(field_name="attributes__attribute_id", lookup_expr="icontains", label="Wyposażenie")

    class Meta:
        model = Room
        fields = ["room_number", "attribute"]


class FreeRoomFilter(filters.FilterSet):
    start_date = filters.DateFilter(method="filter_by_time", label="Data początkowa")
    end_date = filters.DateFilter(method="filter_by_time", label="Data końcowa")
    start_time = filters.TimeFilter(method="filter_by_time", label="Godzina początkowa")
    end_time = filters.TimeFilter(method="filter_by_time", label="Godzina końcowa")
    attribute = filters.CharFilter(
        field_name="attributes__description_pl", lookup_expr="icontains", label="Wyposażenie"
    )
    room_number = filters.CharFilter(field_name="room_number", lookup_expr="icontains", label="Nazwa sali")

    class Meta:
        model = Room
        fields = ["start_date", "end_date", "start_time", "end_time", "attribute", "room_number"]

    def filter_by_time(self, queryset, name, value):
        start_date = self.data.get("start_date")
        start_time = self.data.get("start_time")
        end_date = self.data.get("end_date")
        end_time = self.data.get("end_time")

        if start_date and start_time:
            start_datetime = f"{start_date}T{start_time}"
        else:
            start_datetime = None

        if end_date and end_time:
            end_datetime = f"{end_date}T{end_time}"
        else:
            end_datetime = None

        if start_datetime and end_datetime:
            busy_rooms = Meeting.objects.filter(
                Q(start_time__lt=end_datetime) & Q(end_time__gt=start_datetime)
            ).values_list("room_id", flat=True)
            queryset = queryset.exclude(id__in=busy_rooms)

        return queryset


class GroupFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="Nazwa grupy")
    group_type = filters.ChoiceFilter(choices=Group.GROUP_TYPE_CHOICES, label="Typ grupy")
    admin = filters.CharFilter(field_name="admins__email", lookup_expr="icontains", label="Email administratora")
    member = filters.CharFilter(field_name="members__email", lookup_expr="icontains", label="Email członka")

    class Meta:
        model = Group
        fields = ["name", "group_type", "admin", "member"]
