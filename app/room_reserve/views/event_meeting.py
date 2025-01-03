from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from room_reserve.models import Event, Meeting, Lecturers, Room, Group
from django.utils.dateparse import parse_datetime
from room_reserve.notifications import (
    notify_event_with_meetings_submission,
    notify_admin_event_with_meetings_submission,
)


def create_event_with_meetings(request):
    if request.method == "POST":
        # Collect event data
        event_name = request.POST.get("eventname")
        event_description = request.POST.get("eventdescription")
        event_start_date = request.POST.get("eventdatestart")
        event_end_date = request.POST.get("eventdateend")
        event_logo = request.FILES.get("eventlogo")  # Get the uploaded logo
        selected_group_ids = request.POST.getlist("eventgroups[]")  # Get selected groups

        # Create the event object
        event = Event.objects.create(
            name=event_name,
            description=event_description,
            start_date=event_start_date,
            end_date=event_end_date,
            event_type=Event.GENERAL_EVENT,
            logo=event_logo,  # Save the logo
        )

        # Associate event with selected groups
        selected_groups = Group.objects.filter(id__in=selected_group_ids)
        for group in selected_groups:
            group.events.add(event)

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
            room = Room.objects.filter(id=segment_rooms[i]).first()
            lecturer = Lecturers.objects.filter(id=segment_lecturers[i]).first()
            start_datetime = parse_datetime(f"{segment_dates[i]}T{segment_start_times[i]}")
            end_datetime = parse_datetime(f"{segment_dates[i]}T{segment_end_times[i]}")

            meeting = Meeting.objects.create(
                name_pl=segment_names[i],
                description=segment_descriptions[i],
                start_time=start_datetime,
                end_time=end_datetime,
                capacity=segment_participants[i],
                event=event,
                room=room,
            )

            if lecturer:
                meeting.lecturers.add(lecturer)

            for group in selected_groups:
                group.meetings.add(meeting)

        # Notify user and administrators
        notify_event_with_meetings_submission(user=request.user, event_name=event_name, submitted_by=request.user)
        notify_admin_event_with_meetings_submission(event_name=event_name, submitted_by=request.user)

        messages.success(request, "Event and its segments have been successfully created.")
        return redirect("home")
    else:
        # Obsługa dla metody GET
        groups = Group.objects.all()
        return render(request, "pages/calendar/create_event_with_meetings.html", {"groups": groups})


def edit_event_with_meetings(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    meetings = event.meetings.all()
    rooms = Room.objects.all()
    lecturers = Lecturers.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        # Aktualizacja wydarzenia
        event.name = request.POST.get("eventname")
        event.description = request.POST.get("eventdescription")
        event.start_date = request.POST.get("eventdatestart")
        event.end_date = request.POST.get("eventdateend")
        if request.FILES.get("eventlogo"):
            event.logo = request.FILES.get("eventlogo")

        selected_group_ids = request.POST.getlist("eventgroups[]")
        event.groups.set(Group.objects.filter(id__in=selected_group_ids))
        event.save()

        # Aktualizacja spotkań
        segment_ids = request.POST.getlist("segmentid[]")
        segment_names = request.POST.getlist("segmentname[]")
        segment_lecturers = request.POST.getlist("segmentlecturer[]")
        segment_rooms = request.POST.getlist("segmentroom[]")
        segment_descriptions = request.POST.getlist("segmentdescription[]")
        segment_dates = request.POST.getlist("segmentdate[]")
        segment_start_times = request.POST.getlist("segmenttimestart[]")
        segment_end_times = request.POST.getlist("segmenttimeend[]")
        segment_participants = request.POST.getlist("segmentparticipants[]")

        for i, segment_id in enumerate(segment_ids):
            if segment_id:  # Istniejące spotkanie
                meeting = get_object_or_404(Meeting, id=segment_id)
            else:  # Nowe spotkanie
                meeting = Meeting(event=event)

            meeting.name_pl = segment_names[i]
            meeting.description = segment_descriptions[i]
            meeting.start_time = parse_datetime(f"{segment_dates[i]}T{segment_start_times[i]}")
            meeting.end_time = parse_datetime(f"{segment_dates[i]}T{segment_end_times[i]}")
            meeting.capacity = segment_participants[i]
            meeting.room = Room.objects.filter(id=segment_rooms[i]).first()
            lecturer = Lecturers.objects.filter(id=segment_lecturers[i]).first()
            if lecturer:
                meeting.lecturers.set([lecturer])
            meeting.save()

        messages.success(request, "Wydarzenie i spotkania zostały pomyślnie zaktualizowane.")
        return redirect("event_details", event_id=event.id)

    return render(
        request,
        "pages/calendar/edit_event_with_meetings.html",
        {
            "event": event,
            "meetings": meetings,
            "rooms": rooms,
            "lecturers": lecturers,
            "groups": groups,
        },
    )
