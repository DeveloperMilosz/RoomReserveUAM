from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from room_reserve.models import Event, Meeting, Lecturers, Room, Group, User
from django.utils.dateparse import parse_datetime
from room_reserve.notifications import (
    notify_event_with_meetings_submission,
    notify_admin_event_with_meetings_submission,
)
from django.contrib.auth.decorators import login_required


@login_required
def create_event_with_meetings(request):
    if request.method == "POST":
        # Collect event data
        event_name = request.POST.get("eventname")
        event_description = request.POST.get("eventdescription")
        event_start_date = request.POST.get("eventdatestart")
        event_end_date = request.POST.get("eventdateend")
        event_logo = request.FILES.get("eventlogo")  # Optional logo upload
        selected_group_ids = request.POST.getlist("eventgroups[]")
        selected_organizers_ids = request.POST.getlist("segmentuser[]")  # New functionality

        # Create the event object
        event = Event.objects.create(
            name=event_name,
            description=event_description,
            start_date=event_start_date,
            end_date=event_end_date,
            logo=event_logo,
        )

        # Add organizers to the event
        selected_organizers = User.objects.filter(
            id__in=selected_organizers_ids, user_type__in=["Organizer", "Lecturer"]
        )
        event.organizer.set(selected_organizers)

        # Associate event with selected groups
        selected_groups = Group.objects.filter(id__in=selected_group_ids)
        for group in selected_groups:
            group.events.add(event)

        # Collect segment (meeting) data
        segment_names = request.POST.getlist("segmentname[]")
        segment_rooms = request.POST.getlist("segmentroom[]")
        segment_descriptions = request.POST.getlist("segmentdescription[]")
        segment_dates = request.POST.getlist("segmentdate[]")
        segment_start_times = request.POST.getlist("segmenttimestart[]")
        segment_end_times = request.POST.getlist("segmenttimeend[]")
        segment_participants = request.POST.getlist("segmentparticipants[]")

        # Create each meeting
        for i in range(len(segment_names)):
            room = Room.objects.filter(id=segment_rooms[i]).first()
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

            # Assign organizers to the meeting
            meeting.lecturers.set(selected_organizers)

            # Add meeting to selected groups
            for group in selected_groups:
                group.meetings.add(meeting)

        # Notify the user and administrators
        notify_event_with_meetings_submission(user=request.user, event_name=event_name, submitted_by=request.user)
        notify_admin_event_with_meetings_submission(event_name=event_name, submitted_by=request.user)

        messages.success(request, "Event and its meetings were successfully created.")
        return redirect("home")
    else:
        # Fetch data for the form
        groups = Group.objects.all()
        users = User.objects.filter(user_type__in=["Organizer", "Lecturer"])
        rooms = Room.objects.all()
        return render(
            request,
            "pages/calendar/create_event_with_meetings.html",
            {
                "groups": groups,
                "users": users,
                "rooms": rooms,
            },
        )


@login_required
def edit_event_with_meetings(request, event_id):
    # Fetch the event and related details
    event = get_object_or_404(Event, pk=event_id)
    meetings = event.meetings.all()  # Meetings linked to this event
    rooms = Room.objects.all()  # All available rooms
    groups = Group.objects.all()  # All available groups
    users = User.objects.filter(user_type__in=["Organizer", "Lecturer"])  # Users eligible as organizers

    # Permission check: Only Admins and event organizers can edit
    if not (request.user.user_type == "Admin" or request.user in event.organizer.all()):
        print(f"User Type: {request.user.user_type}")
        print(f"User: {request.user} not in Event Organizers: {event.organizer.all()}")
        return JsonResponse({"error": "Permission denied", "reason": "User lacks Admin role or is not an Organizer."}, status=403)

    if request.method == "POST":
        try:
            # Update event details
            event.name = request.POST.get("eventname")
            event.description = request.POST.get("eventdescription")
            event.start_date = request.POST.get("eventdatestart")
            event.end_date = request.POST.get("eventdateend")

            if request.FILES.get("eventlogo"):
                event.logo = request.FILES.get("eventlogo")

            event.save()

            # Update event organizers
            selected_organizers_ids = request.POST.getlist("segmentuser[]")
            selected_organizers = User.objects.filter(id__in=selected_organizers_ids, user_type__in=["Organizer", "Lecturer"])
            event.organizer.set(selected_organizers)

            # Update event groups
            selected_group_ids = request.POST.getlist("eventgroups[]")
            selected_groups = Group.objects.filter(id__in=selected_group_ids)

            for group in groups:
                if group in selected_groups:
                    group.events.add(event)
                else:
                    group.events.remove(event)

            # Update meetings
            segment_ids = request.POST.getlist("segmentid[]")
            segment_names = request.POST.getlist("segmentname[]")
            segment_rooms = request.POST.getlist("segmentroom[]")
            segment_descriptions = request.POST.getlist("segmentdescription[]")
            segment_dates = request.POST.getlist("segmentdate[]")
            segment_start_times = request.POST.getlist("segmenttimestart[]")
            segment_end_times = request.POST.getlist("segmenttimeend[]")
            segment_participants = request.POST.getlist("segmentparticipants[]")

            for i, segment_id in enumerate(segment_ids):
                meeting = Meeting.objects.filter(id=segment_id).first() if segment_id else Meeting(event=event)

                meeting.name_pl = segment_names[i]
                meeting.description = segment_descriptions[i]
                meeting.start_time = parse_datetime(f"{segment_dates[i]}T{segment_start_times[i]}")
                meeting.end_time = parse_datetime(f"{segment_dates[i]}T{segment_end_times[i]}")
                meeting.capacity = segment_participants[i]
                meeting.room = Room.objects.filter(id=segment_rooms[i]).first()
                meeting.save()

            messages.success(request, "Event and its meetings were successfully updated.")
            return redirect("event_details", event_id=event.id)

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    # Render the edit page
    return render(
        request,
        "pages/calendar/edit_event_with_meetings.html",
        {
            "event": event,
            "meetings": meetings,
            "rooms": rooms,
            "groups": groups,
            "users": users,
        },
    )