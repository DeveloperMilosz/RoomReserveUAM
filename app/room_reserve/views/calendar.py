from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from room_reserve.models import Meeting, Event, Room, Lecturers
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect, get_object_or_404
from room_reserve.forms.calendar import MeetingForm, EventForm

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
            'in_event': meeting.event is not None,
            'event_name': meeting.event.name if meeting.event else None
        }
        for meeting in meetings
    ]
    return JsonResponse(events, safe=False)

def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    event = meeting.event
    return render(request, 'pages/calendar/meeting_details.html', {'meeting': meeting, 'event': event})

def new_meeting(request):
    rooms = Room.objects.all()
    events = Event.objects.all()
    lecturers = Lecturers.objects.all()
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MeetingForm()
    return render(request, 'pages/calendar/new_meeting.html', {'form': form, 'rooms': rooms, 'events': events, 'lecturers': lecturers})


def new_event(request):
    lecturers = Lecturers.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'pages/calendar/new_event.html', {'form': form, 'lecturers': lecturers})