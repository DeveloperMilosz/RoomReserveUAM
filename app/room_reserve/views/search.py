from django.shortcuts import render
from room_reserve.models import Meeting, Event, Room
from room_reserve.filters import MeetingFilter, EventFilter, RoomFilter, FreeRoomFilter


def search_meetings(request):
    """Wyszukaj spotkania."""
    if request.GET:  # Wyświetl wyniki tylko, jeśli są parametry GET
        meeting_filter = MeetingFilter(request.GET, queryset=Meeting.objects.all())
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
