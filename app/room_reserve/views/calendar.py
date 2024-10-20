from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from room_reserve.models.calendar import Meeting, Room
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect
from .forms import MeetingForm

import json

def get_meetings(request):
    meetings = Meeting.objects.all()
    events = []
    for meeting in meetings:
        events.append({
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
