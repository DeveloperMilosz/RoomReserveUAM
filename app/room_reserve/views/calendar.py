from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.db.models import Q
from room_reserve.models import Meeting, Event, Room, Lecturers, RoomAttribute, Group, User
from room_reserve.forms.calendar import MeetingForm, EventForm, EditMeetingForm
from datetime import datetime, timedelta
from room_reserve.notifications import (
    notify_meeting_submission,
    notify_admin_meeting_submission,
    notify_event_submission,
    notify_admin_event_submission,
)
from django.contrib import messages
import json


# @login_required
# def new_meeting(request):
#     rooms = Room.objects.all()
#     events = Event.objects.all()
#     lecturers = Lecturers.objects.all()
#     if request.method == "POST":
#         form = MeetingForm(request.POST)
#         if form.is_valid():
#             meeting = form.save(commit=False)
#             meeting.is_approved = False
#             meeting.submitted_by = request.user
#             meeting.save()
#             form.save_m2m()
#             return redirect("home")
#     else:
#         form = MeetingForm()
#     return render(
#         request,
#         "pages/calendar/new_meeting.html",
#         {"form": form, "rooms": rooms, "events": events, "lecturers": lecturers},
#     )


def get_meetings(request):
    meetings = (
        Meeting.objects.select_related("room", "event")
        .prefetch_related("lecturers")
        .filter(is_approved=True)
        .order_by("start_time")
    )
    events = []
    for meeting in meetings:
        event_data = {
            "id": meeting.id,
            "start_time": meeting.start_time.isoformat(),
            "end_time": meeting.end_time.isoformat(),
            "title": meeting.name_pl,
            "color": meeting.color,
            "room": meeting.room.room_number if meeting.room else None,
            "lecturer": [f"{lecturer.first_name} {lecturer.last_name}" for lecturer in meeting.lecturers.all()],
        }

        if meeting.event and meeting.event.logo:
            event_data["logo"] = request.build_absolute_uri(meeting.event.logo.url)
        else:
            event_data["logo"] = None

        events.append(event_data)

    return JsonResponse(events, safe=False)


def room_schedule(request, room_id):
    """
    Fetch and display the schedule for a specific room, including the current meeting
    and the next meeting, with event details.
    """
    room = get_object_or_404(Room, id=room_id)

    current_meeting = (
        Meeting.objects.filter(start_time__lte=now(), end_time__gte=now(), room=room).select_related("event").first()
    )

    next_meeting = (
        Meeting.objects.filter(start_time__gt=now(), room=room).select_related("event").order_by("start_time").first()
    )

    return render(
        request,
        "pages/calendar/room_schedule.html",
        {
            "room": room,
            "current_meeting": current_meeting,
            "next_meeting": next_meeting,
        },
    )


@login_required
def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    event = meeting.event
    all_groups = Group.objects.all()
    lecturers = meeting.lecturers.all()  # Fetch associated lecturers

    if request.method == "POST":
        selected_group_ids = request.POST.getlist("groups")
        selected_groups = Group.objects.filter(id__in=selected_group_ids)
        meeting.assigned_groups.set(selected_groups)
        meeting.save()
        return redirect("meeting_details", meeting_id=meeting.id)

    return render(
        request,
        "pages/calendar/meeting_details.html",
        {
            "meeting": meeting,
            "event": event,
            "all_groups": all_groups,
            "lecturers": lecturers,  # Pass lecturers to the template
        },
    )


def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    meetings = event.meetings.all()
    organizers = event.organizer.all()  # Assuming organizer is a ManyToManyField
    return render(request, "pages/calendar/event_details.html", {
        "event": event,
        "meetings": meetings,
        "organizers": organizers,
    })


def room_details(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    attributes = room.attributes.all()

    room_number_parts = room.room_number.split(".")
    floor = "parter" if room_number_parts[0] == "0" else room_number_parts[0]

    return render(
        request,
        "pages/calendar/room_details.html",
        {
            "room": room,
            "attributes": attributes,
            "floor": floor,
        },
    )


def new_meeting(request):
    """
    Create a new meeting with the option to select multiple users as organizers or lecturers.
    """
    rooms = Room.objects.all()
    events = Event.objects.all()
    groups = Group.objects.all()
    users = User.objects.filter(user_type__in=["Lecturer", "Organizer"])  # Filter users by type

    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting_data = form.cleaned_data

            # Extract form fields
            is_recurring = meeting_data.get("is_recurring")
            frequency_select = meeting_data.get("frequency_select")
            days_of_week = meeting_data.get("days_of_week")
            cycle_end_date = meeting_data.get("cycle_end_date")
            start_time = meeting_data.get("start_time")
            end_time = meeting_data.get("end_time")
            selected_lecturers = meeting_data.get("lecturers")
            selected_groups = meeting_data.get("groups")

            # Handle recurring meetings
            if is_recurring and frequency_select and cycle_end_date:
                current_date = start_time.date()
                while current_date <= cycle_end_date:
                    should_add = False

                    if frequency_select == "daily":
                        should_add = True
                    elif frequency_select == "weekly":
                        should_add = (current_date - start_time.date()).days % 7 == 0
                    elif frequency_select == "biweekly":
                        should_add = (current_date - start_time.date()).days % 14 == 0
                    elif frequency_select == "monthly":
                        should_add = current_date.day == start_time.date().day
                    elif frequency_select == "custom_days":
                        should_add = str(current_date.weekday()) in days_of_week

                    if should_add:
                        meeting = Meeting.objects.create(
                            name_pl=meeting_data["name_pl"],
                            name_en=meeting_data["name_en"],
                            start_time=datetime.combine(current_date, start_time.time()),
                            end_time=datetime.combine(current_date, end_time.time()),
                            room=meeting_data["room"],
                            description=meeting_data["description"],
                            color=meeting_data["color"],
                            capacity=meeting_data["capacity"],
                            is_updated=False,
                            is_approved=False,
                            event=meeting_data.get("event"),
                            submitted_by=request.user,
                        )

                        # Add lecturers and groups
                        if selected_lecturers:
                            meeting.lecturers.set(selected_lecturers)

                        if selected_groups:
                            meeting.groups.set(selected_groups)

                    # Advance to the next date
                    if frequency_select in ["daily", "weekly", "biweekly", "custom_days"]:
                        current_date += timedelta(days=1)
                    elif frequency_select == "monthly":
                        # Advance to the next month
                        next_month = (current_date.month % 12) + 1
                        current_date = current_date.replace(month=next_month)

            # Handle a single meeting
            else:
                meeting = form.save(commit=False)
                meeting.submitted_by = request.user
                meeting.is_approved = False
                meeting.save()
                form.save_m2m()  # Save the many-to-many relationships

            # Notify user and admins
            notify_meeting_submission(request.user, meeting_data["name_pl"], submitted_by=request.user)
            notify_admin_meeting_submission(meeting_data["name_pl"], submitted_by=request.user)

            messages.success(request, "Meeting request submitted successfully.")
            return redirect("home")
        else:
            messages.error(request, "There was an error submitting the meeting request.")
    else:
        form = MeetingForm()

    return render(
        request,
        "pages/calendar/new_meeting.html",
        {
            "form": form,
            "rooms": rooms,
            "events": events,
            "groups": groups,
            "users": users,
        },
    )


@login_required
def edit_meeting(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    rooms = Room.objects.all()
    events = Event.objects.all()
    users = User.objects.filter(user_type__in=["Lecturer", "Organizer"])
    groups = Group.objects.all()  # Fetch all groups

    if request.method == "POST":
        form = EditMeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save(commit=False)
            selected_groups = form.cleaned_data.get("groups")  # Ensure this matches your form fields
            meeting.assigned_groups.set(selected_groups)  # Use 'assigned_groups' here
            meeting.save()
            form.save_m2m()
            messages.success(request, "Meeting updated successfully.")
            return redirect("meeting_details", meeting_id=meeting.id)
        else:
            messages.error(request, "There was an error updating the meeting.")
    else:
        form = EditMeetingForm(instance=meeting)

    return render(
        request,
        "pages/calendar/edit_meeting.html",
        {
            "form": form,
            "meeting": meeting,
            "rooms": rooms,
            "events": events,
            "lecturers": users,
            "groups": groups,
        },
    )


def new_event(request):
    users = User.objects.filter(user_type__in=["Lecturer", "Organizer"])  # Fetch appropriate users

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()

            # Associate the event with selected organizers/lecturers
            selected_users = request.POST.getlist("organizer")
            event.organizer.set(User.objects.filter(id__in=selected_users))

            return redirect("home")
    else:
        form = EventForm()

    return render(
        request,
        "pages/calendar/new_event.html",
        {"form": form, "users": users},
    )

    return render(
        request,
        "pages/calendar/new_event.html",
        {
            "form": form,
            "lecturers": lecturers,
            "groups": groups,
            "users": users,
        },
    )

def delete_meeting(request, meeting_id):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=meeting_id)
        meeting.delete()
        return JsonResponse({"message": "Meeting deleted successfully"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def search_view(request):
    search_type = request.GET.get("search_type", "")
    meetings, events, available_rooms = [], [], []

    if search_type == "meetings":
        meeting_query = request.GET.get("meeting_query", "").strip()
        meeting_type = request.GET.get("meeting_type", "").strip()
        start_date_meeting = request.GET.get("start_date_meeting", "")
        end_date_meeting = request.GET.get("end_date_meeting", "")
        lecturer = request.GET.get("lecturer", "").strip()
        room = request.GET.get("room", "").strip()
        meeting_capacity = request.GET.get("meeting_capacity", "")
        room_capacity = request.GET.get("room_capacity", "")
        event_id = request.GET.get("event", "").strip()

        meeting_filters = Q(is_approved=True)
        if meeting_query:
            meeting_filters &= Q(name_pl__icontains=meeting_query) | Q(name_en__icontains=meeting_query)
        if meeting_type:
            meeting_filters &= Q(meeting_type=meeting_type)
        if start_date_meeting and end_date_meeting:
            meeting_filters &= Q(start_time__gte=start_date_meeting, end_time__lte=end_date_meeting)
        if lecturer:
            meeting_filters &= Q(lecturers__first_name__icontains=lecturer) | Q(
                lecturers__last_name__icontains=lecturer
            )
        if room:
            meeting_filters &= Q(room__id=room)
        if meeting_capacity:
            meeting_filters &= Q(capacity__gte=meeting_capacity)
        if room_capacity:
            meeting_filters &= Q(room__capacity__gte=room_capacity)
        if event_id:
            meeting_filters &= Q(event__id=event_id)

        meetings = Meeting.objects.filter(meeting_filters).distinct()

    elif search_type == "events":
        event_query = request.GET.get("event_query", "").strip()
        event_type = request.GET.get("event_type", "").strip()
        start_date_event = request.GET.get("start_date_event", "")
        end_date_event = request.GET.get("end_date_event", "")

        event_filters = Q()
        if event_query:
            event_filters &= Q(name__icontains=event_query)
        if event_type:
            event_filters &= Q(event_type=event_type)
        if start_date_event and end_date_event:
            event_filters &= Q(start_date__gte=start_date_event, end_date__lte=end_date_event)
        events = Event.objects.filter(event_filters)

    elif search_type == "rooms":
        room_query = request.GET.get("room_query", "").strip()
        start_date_room = request.GET.get("start_date_room", "")
        end_date_room = request.GET.get("end_date_room", "")

        if start_date_room and end_date_room:
            busy_rooms = Meeting.objects.filter(
                Q(start_time__lt=end_date_room) & Q(end_time__gt=start_date_room)
            ).values_list("room_id", flat=True)
            available_rooms = Room.objects.exclude(id__in=busy_rooms)
        else:
            available_rooms = Room.objects.all()
        if room_query:
            available_rooms = available_rooms.filter(room_number__icontains=room_query)

    all_rooms = Room.objects.all()
    all_lecturers = Lecturers.objects.all()
    all_events = Event.objects.all()

    return render(
        request,
        "pages/calendar/search.html",
        {
            "meetings": meetings,
            "events": events,
            "available_rooms": available_rooms,
            "all_rooms": all_rooms,
            "all_lecturers": all_lecturers,
            "all_events": all_events,
            "meeting_query": request.GET.get("meeting_query", ""),
            "event_query": request.GET.get("event_query", ""),
            "room_query": request.GET.get("room_query", ""),
            "meeting_type": request.GET.get("meeting_type", ""),
            "event_type": request.GET.get("event_type", ""),
            "start_date_meeting": request.GET.get("start_date_meeting", ""),
            "end_date_meeting": request.GET.get("end_date_meeting", ""),
            "start_date_event": request.GET.get("start_date_event", ""),
            "end_date_event": request.GET.get("end_date_event", ""),
            "start_date_room": request.GET.get("start_date_room", ""),
            "end_date_room": request.GET.get("end_date_room", ""),
            "lecturer": request.GET.get("lecturer", ""),
            "room": request.GET.get("room", ""),
            "meeting_capacity": request.GET.get("meeting_capacity", ""),
            "room_capacity": request.GET.get("room_capacity", ""),
            "event": request.GET.get("event", ""),
        },
    )


@login_required
def cancel_meeting(request, meeting_id):
    """
    Widok odwoływania spotkania.
    """
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # Sprawdzenie, czy użytkownik może odwołać spotkanie
    if request.user != meeting.submitted_by and not request.user.is_staff:
        return JsonResponse({"error": "Nie masz uprawnień do odwołania tego spotkania."}, status=403)

    meeting.is_canceled = True
    meeting.save()

    # Przekierowanie na stronę edycji spotkania
    return redirect("edit_meeting", meeting_id=meeting.id)


@login_required
def restore_meeting(request, meeting_id):
    """
    Widok przywracania odwołanego spotkania.
    """
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # Sprawdzenie, czy użytkownik może przywrócić spotkanie
    if request.user != meeting.submitted_by and not request.user.is_staff:
        return JsonResponse({"error": "Nie masz uprawnień do przywrócenia tego spotkania."}, status=403)

    meeting.is_canceled = False
    meeting.save()

    # Przekierowanie na stronę edycji spotkania
    return redirect("edit_meeting", meeting_id=meeting.id)


def about_view(request):
    return render(request, 'pages/about.html')