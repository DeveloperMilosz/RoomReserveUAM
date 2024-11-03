from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from room_reserve.models import Meeting, Room  # Zaktualizowane na import z modelu głównego
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect, get_object_or_404
from room_reserve.forms.meeting import MeetingForm

import json

def get_meetings(request):
    meetings = Meeting.objects.select_related('room', 'event').prefetch_related('lecturers').all()
    events = [
        {
            'id': meeting.id,
            'title': meeting.name_pl,
            'meeting_type': meeting.meeting_type,
            'start_time': meeting.start_time.isoformat(),
            'end_time': meeting.end_time.isoformat(),
            'name_en': meeting.name_en,
            'room': meeting.room.room_number if meeting.room else None,
            'description': meeting.description,
            'lecturers': [f"{lecturer.first_name} {lecturer.last_name}" for lecturer in meeting.lecturers.all()],
            'capacity': meeting.capacity,
            'color': meeting.color,
            'is_updated': meeting.is_updated,
            'in_event': meeting.event is not None,  # Check if the meeting has an associated event
            'event_name': meeting.event.name if meeting.event else None  # Get event name if exists
        }
        for meeting in meetings
    ]
    return JsonResponse(events, safe=False)

def new_meeting(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MeetingForm()
    return render(request, 'pages/calendar/new_meeting.html', {'form': form, 'rooms': rooms})

def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    event = meeting.event  # Access the associated event directly
    return render(request, 'pages/calendar/meeting_details.html', {'meeting': meeting, 'event': event})
