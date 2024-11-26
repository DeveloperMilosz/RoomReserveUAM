from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from room_reserve.models.calendar import Meeting, Room
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect
from .forms import MeetingForm
from django.shortcuts import render, get_object_or_404

import json

def get_meetings(request):
    meetings = Meeting.objects.all()
    events = []
    for meeting in meetings:
        events.append({
            'id': meeting.id,
            'title': meeting.name_pl,
            'start_time': meeting.start_time.isoformat(),
            'end_time': meeting.end_time.isoformat(),
        })
    return JsonResponse(events, safe=False)

def new_meeting(request):
    rooms = Room.objects.all()  # Pobierz wszystkie pokoje
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Przekierowanie po zapisaniu
    else:
        form = MeetingForm()
    return render(request, 'pages/calendar/new_meeting.html', {'form': form, 'rooms': rooms})

def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    return render(request, 'pages/calendar/meeting_details.html', {'meeting': meeting})

# def edit_meeting(request, meeting_id):
#     editmeeting = get_object_or_404(Meeting, pk=meeting_id)
#     return render(request, 'pages/calendar/edit_meeting.html', {'meeting': editmeeting})

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