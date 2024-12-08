from django.shortcuts import render, redirect
from django.contrib import messages
from room_reserve.models import Event, Meeting, Lecturers, Room
import json
from django.utils.dateparse import parse_datetime

def create_event_with_meetings(request):
    if request.method == "POST":
        # Collect event data
        event_name = request.POST.get("eventname")
        event_description = request.POST.get("eventdescription")
        event_start_date = request.POST.get("eventdatestart")
        event_end_date = request.POST.get("eventdateend")
        event_participants = request.POST.get("participants")

        # Create the event object
        event = Event.objects.create(
            name=event_name,
            description=event_description,
            start_date=event_start_date,
            end_date=event_end_date,
            event_type=Event.GENERAL_EVENT
        )

        # Collect segment (meeting) data
        segment_names = request.POST.getlist("segmentname[]")
        segment_lecturers = request.POST.getlist("segmentlecturer[]")
        segment_rooms = request.POST.getlist("segmentroom[]")
        segment_descriptions = request.POST.getlist("segmentdescription[]")
        segment_dates = request.POST.getlist("segmentdate[]")
        segment_start_times = request.POST.getlist("segmenttimestart[]")
        segment_end_times = request.POST.getlist("segmenttimeend[]")
        segment_participants = request.POST.getlist("segmentparticipants[]")

        # Iterate over each segment and create meetings
        for i in range(len(segment_names)):
            # Get the related objects (lecturer and room)
            room = Room.objects.filter(id=segment_rooms[i]).first()
            lecturer = Lecturers.objects.filter(id=segment_lecturers[i]).first()

            # Parse datetime fields
            start_datetime = parse_datetime(f"{segment_dates[i]}T{segment_start_times[i]}")
            end_datetime = parse_datetime(f"{segment_dates[i]}T{segment_end_times[i]}")

            # Create the meeting
            meeting = Meeting.objects.create(
                name_pl=segment_names[i],
                description=segment_descriptions[i],
                start_time=start_datetime,
                end_time=end_datetime,
                capacity=segment_participants[i],
                event=event,  # Link the meeting to the event
                room=room,    # Link the meeting to the room
            )

            # Add lecturer to the meeting
            if lecturer:
                meeting.lecturers.add(lecturer)

        # Success message and redirect
        messages.success(request, "Event and its segments have been successfully created.")
        return redirect("home")

    # Prepare data for the form
    rooms = Room.objects.all()
    lecturers = Lecturers.objects.all()
    return render(request, "pages/calendar/create_event_with_meetings.html", {
        "rooms": rooms,
        "lecturers": lecturers,
    })