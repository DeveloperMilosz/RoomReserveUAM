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


def edit_meeting(request, meeting_id):
    # Fetch the existing meeting object by ID
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    
    if request.method == 'POST':
        # Initialize the form with POST data and bind it to the existing meeting instance
        form = MeetingForm(request.POST, instance=meeting)
        
        if form.is_valid():
            # Save changes if the form is valid
            form.save()
            return redirect('meeting_details', meeting_id=meeting.id)  # Redirect to the meeting details page or home page
    else:
        # Initialize the form with the existing meeting instance for GET requests
        form = MeetingForm(instance=meeting)
    
    # Render the edit page with the form and meeting instance
    return render(request, 'pages/calendar/edit_meeting.html', {'form': form, 'meeting': meeting})

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

def delete_meeting(request, meeting_id):
    # Ensure the user is authenticated or has the right permissions
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=meeting_id)
        meeting.delete()
        return JsonResponse({'message': 'Meeting deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)