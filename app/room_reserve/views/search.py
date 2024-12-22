from django.shortcuts import render
from room_reserve.models import Meeting, Event, Room, Group
from room_reserve.filters import MeetingFilter, EventFilter, RoomFilter, FreeRoomFilter, GroupFilter
from django.http import JsonResponse


def search_meetings(request):
    """Wyszukaj spotkania."""
    if request.GET:
        meeting_filter = MeetingFilter(request.GET, queryset=Meeting.objects.all().order_by("start_time"))
    else:
        meeting_filter = MeetingFilter(queryset=Meeting.objects.none())  
    return render(request, "pages/search/search_meetings.html", {"filter": meeting_filter})


def search_events(request):
    """Wyszukaj wydarzenia."""
    if request.GET:
        event_filter = EventFilter(request.GET, queryset=Event.objects.all())
    else:
        event_filter = EventFilter(queryset=Event.objects.none())  
    
    # Dodaj URL do logo
    for event in event_filter.qs:
        event.logo_url = event.logo.url if event.logo else None
    
    return render(request, "pages/search/search_events.html", {"filter": event_filter})


def search_rooms(request):
    """Wyszukaj sale."""
    if request.GET:  
        room_filter = RoomFilter(request.GET, queryset=Room.objects.all())
    else:
        room_filter = RoomFilter(queryset=Room.objects.none())  
    return render(request, "pages/search/search_rooms.html", {"filter": room_filter})


def search_free_rooms(request):
    """Wyszukaj wolne sale."""
    if request.GET:  
        room_filter = FreeRoomFilter(request.GET, queryset=Room.objects.all())
    else:
        room_filter = FreeRoomFilter(queryset=Room.objects.none())  
    return render(request, "pages/search/search_free_rooms.html", {"filter": room_filter})


def search_groups(request):
    if request.GET:  
        group_filter = GroupFilter(request.GET, queryset=Group.objects.all())
    else:
        group_filter = GroupFilter(queryset=Group.objects.none())  
    return render(request, "pages/search/search_groups.html", {"filter": group_filter})


def api_search_meetings(request):
    meeting_filter = MeetingFilter(
        request.GET,
        queryset=Meeting.objects.select_related("room", "event")
        .prefetch_related("lecturers")
        .filter(is_approved=True)
        .order_by("start_time")
    )
    data = [
        {
            "id": meeting.id,
            "start_time": meeting.start_time.isoformat(),
            "end_time": meeting.end_time.isoformat(),
            "title": meeting.name_pl,
            "color": meeting.color,
            "room": meeting.room.room_number if meeting.room else None,
            "logo": request.build_absolute_uri(meeting.event.logo.url) if meeting.event and meeting.event.logo else None,
            "lecturers": [
                f"{lecturer.first_name} {lecturer.last_name}" for lecturer in meeting.lecturers.all()
            ],
            "event_name": meeting.event.name if meeting.event else None,
            "event_id": meeting.event.id if meeting.event else None,
        }
        for meeting in meeting_filter.qs
    ]
    return JsonResponse(data, safe=False)