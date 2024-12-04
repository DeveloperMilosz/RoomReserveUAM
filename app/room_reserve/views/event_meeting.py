from django.shortcuts import render, redirect
from django.contrib import messages
from room_reserve.models import Event, Meeting, Lecturers

def create_event_with_meetings(request):
    if request.method == "POST":
        # Extract event details from the form
        event_name = request.POST.get("eventname")
        event_description = request.POST.get("eventdescription")
        start_date = request.POST.get("eventdatestart")
        end_date = request.POST.get("eventdateend")
        participants = request.POST.get("participants")

        # Create the event
        event = Event.objects.create(
            name=event_name,
            description=event_description,
            start_date=start_date,
            end_date=end_date,
            event_type=Event.GENERAL_EVENT  # Set default event type
        )

        # Extract meeting details
        segment_names = request.POST.getlist("segmentname[]")
        segment_lecturers = request.POST.getlist("segmentlecturer[]")
        segment_descriptions = request.POST.getlist("segmentdescription[]")
        segment_dates = request.POST.getlist("segmentdate[]")
        segment_start_times = request.POST.getlist("segmenttimestart[]")
        segment_end_times = request.POST.getlist("segmenttimeend[]")
        segment_participants = request.POST.getlist("segmentparticipants[]")

        # Create meetings for the event
        for i in range(len(segment_names)):
            # Lookup lecturer by name (update as necessary to match your logic)
            lecturer_name = segment_lecturers[i]
            lecturer = Lecturers.objects.filter(first_name=lecturer_name).first()

            # Create the meeting
            meeting = Meeting.objects.create(
                name_pl=segment_names[i],
                description=segment_descriptions[i],
                start_time=f"{segment_dates[i]} {segment_start_times[i]}",
                end_time=f"{segment_dates[i]} {segment_end_times[i]}",
                capacity=segment_participants[i],
                event=event,
            )

            # Associate lecturer with the meeting
            if lecturer:
                meeting.lecturers.add(lecturer)

        messages.success(request, "Event and meetings created successfully!")
        return redirect("home")

    return render(request, "pages/calendar/create_event_with_meetings.html")
