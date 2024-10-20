from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from room_reserve.models.calendar import Meeting, Room
from django.utils.dateparse import parse_datetime
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