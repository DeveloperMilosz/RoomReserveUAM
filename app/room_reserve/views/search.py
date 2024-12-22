from django.shortcuts import render
from room_reserve.models import Meeting, Event, Room, Group
from room_reserve.filters import MeetingFilter, EventFilter, RoomFilter, FreeRoomFilter, GroupFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response


def search_meetings(request):
    """Wyszukaj spotkania."""
    if request.GET:  # Wyświetl wyniki tylko, jeśli są parametry GET
        meeting_filter = MeetingFilter(request.GET, queryset=Meeting.objects.all().order_by("start_time"))
    else:
        meeting_filter = MeetingFilter(queryset=Meeting.objects.none())  # Pusty queryset bez filtrów
    return render(request, "pages/search/search_meetings.html", {"filter": meeting_filter})


def search_events(request):
    """Wyszukaj wydarzenia."""
    if request.GET:  # Wyświetl wyniki tylko, jeśli są parametry GET
        event_filter = EventFilter(request.GET, queryset=Event.objects.all())
    else:
        event_filter = EventFilter(queryset=Event.objects.none())  # Pusty queryset bez filtrów
    return render(request, "pages/search/search_events.html", {"filter": event_filter})


def search_rooms(request):
    """Wyszukaj sale."""
    if request.GET:  # Wyświetl wyniki tylko, jeśli są parametry GET
        room_filter = RoomFilter(request.GET, queryset=Room.objects.all())
    else:
        room_filter = RoomFilter(queryset=Room.objects.none())  # Pusty queryset bez filtrów
    return render(request, "pages/search/search_rooms.html", {"filter": room_filter})


def search_free_rooms(request):
    """Wyszukaj wolne sale."""
    if request.GET:  # Wyświetl wyniki tylko, jeśli są parametry GET
        room_filter = FreeRoomFilter(request.GET, queryset=Room.objects.all())
    else:
        room_filter = FreeRoomFilter(queryset=Room.objects.none())  # Pusty queryset bez filtrów
    return render(request, "pages/search/search_free_rooms.html", {"filter": room_filter})


def search_groups(request):
    """Wyszukaj grupy."""
    if request.GET:  # Wyświetl wyniki tylko, jeśli są parametry GET
        group_filter = GroupFilter(request.GET, queryset=Group.objects.all())
    else:
        group_filter = GroupFilter(queryset=Group.objects.none())  # Pusty queryset bez filtrów
    return render(request, "pages/search/search_groups.html", {"filter": group_filter})


# API Endpoints
@api_view(["GET"])
def api_search_meetings(request):
    """API: Wyszukaj spotkania."""
    meeting_filter = MeetingFilter(request.GET, queryset=Meeting.objects.all().order_by("start_time"))
    data = meeting_filter.qs.values()  # Pobieramy przefiltrowane dane jako słowniki
    return Response(data)


@api_view(["GET"])
def api_search_events(request):
    """API: Wyszukaj wydarzenia."""
    event_filter = EventFilter(request.GET, queryset=Event.objects.all())
    data = event_filter.qs.values()
    return Response(data)


@api_view(["GET"])
def api_search_rooms(request):
    """API: Wyszukaj sale."""
    room_filter = RoomFilter(request.GET, queryset=Room.objects.all())
    data = room_filter.qs.values()
    return Response(data)


@api_view(["GET"])
def api_search_free_rooms(request):
    """API: Wyszukaj wolne sale."""
    room_filter = FreeRoomFilter(request.GET, queryset=Room.objects.all())
    data = room_filter.qs.values()
    return Response(data)


@api_view(["GET"])
def api_search_groups(request):
    """API: Wyszukaj grupy."""
    group_filter = GroupFilter(request.GET, queryset=Group.objects.all())
    data = group_filter.qs.values("id", "name", "group_type", "admins__email", "members__email")
    return Response(data)
