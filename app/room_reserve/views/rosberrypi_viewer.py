from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now, localtime
from room_reserve.models import Room, Meeting

def room_schedule_view(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    current_time = localtime(now())  # Use local time for consistency

    # Get the current meeting or None if there's no ongoing meeting
    current_meeting = Meeting.objects.filter(
        room=room, start_time__lte=current_time, end_time__gte=current_time
    ).first()

    # Get the next meeting regardless of whether there's a current meeting
    next_meeting = Meeting.objects.filter(
        room=room, start_time__gt=current_time
    ).order_by('start_time').first()

    context = {
        "room": room,
        "current_meeting": current_meeting,
        "next_meeting": next_meeting,
    }
    return render(request, "pages/calendar/viewer.html", context)