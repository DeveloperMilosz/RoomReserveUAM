from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime, now
from room_reserve.models import Room, Meeting

def room_schedule_view(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    current_time = localtime(now())

    # Pobieramy maksymalnie 2 spotkania, które jeszcze się nie zakończyły
    # i które mają najbliższy czas zakończenia
    soonest_ending_meetings = Meeting.objects.filter(
        room=room,
        end_time__gte=current_time   # spotkania, które jeszcze się nie skończyły
    ).order_by('end_time')[:2]       # sortujemy po end_time rosnąco i bierzemy 2

    return render(request, "pages/calendar/viewer.html", {
        "room": room,
        "soonest_ending_meetings": soonest_ending_meetings,
    })
