from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.db.models import Q
from room_reserve.models import Meeting, Event, Room, Lecturers
from room_reserve.forms.calendar import MeetingForm, EventForm, EditMeetingForm
from datetime import datetime, timedelta
import json


@login_required
def new_meeting(request):
    rooms = Room.objects.all()
    events = Event.objects.all()
    lecturers = Lecturers.objects.all()
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.is_approved = False  # Domyślnie wniosek niezatwierdzony
            meeting.submitted_by = request.user  # Zapisz obecnie zalogowanego użytkownika
            meeting.save()
            form.save_m2m()  # Zapisz powiązania Many-to-Many
            return redirect("home")
    else:
        form = MeetingForm()
    return render(
        request,
        "pages/calendar/new_meeting.html",
        {"form": form, "rooms": rooms, "events": events, "lecturers": lecturers},
    )


def get_meetings(request):
    meetings = Meeting.objects.select_related("room", "event").prefetch_related("lecturers").filter(is_approved=True).order_by("start_time")
    events = [
        {
            "id": meeting.id,
            "start_time": meeting.start_time.isoformat(),
            "end_time": meeting.end_time.isoformat(),
            "title": meeting.name_pl,
            "color": meeting.color,
        }
        for meeting in meetings
    ]
    return JsonResponse(events, safe=False)


def room_schedule(request, room_id):
    """
    Fetch and display the schedule for a specific room, including the current meeting
    and the next meeting, with event details.
    """
    room = get_object_or_404(Room, id=room_id)

    # Fetch the current meeting (if one is ongoing)
    current_meeting = (
        Meeting.objects.filter(start_time__lte=now(), end_time__gte=now(), room=room).select_related("event").first()
    )

    # Fetch the next meeting (if one is scheduled in the future)
    next_meeting = (
        Meeting.objects.filter(start_time__gt=now(), room=room).select_related("event").order_by("start_time").first()
    )

    # Render the template with the meetings and room context
    return render(
        request,
        "pages/calendar/room_schedule.html",
        {
            "room": room,
            "current_meeting": current_meeting,
            "next_meeting": next_meeting,
        },
    )


def meeting_details(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    event = meeting.event
    return render(request, "pages/calendar/meeting_details.html", {"meeting": meeting, "event": event})


def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    meetings = event.meetings.all()
    return render(request, "pages/calendar/event_details.html", {"event": event, "meetings": meetings})


def new_meeting(request):
    rooms = Room.objects.all()
    events = Event.objects.all()
    lecturers = Lecturers.objects.all()

    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting_data = form.cleaned_data

            is_recurring = meeting_data.get("is_recurring")
            frequency_select = meeting_data.get("frequency_select")
            days_of_week = meeting_data.get("days_of_week")
            cycle_end_date = meeting_data.get("cycle_end_date")
            start_time = meeting_data.get("start_time")
            end_time = meeting_data.get("end_time")
            selected_lecturers = meeting_data.get("lecturers")

            if is_recurring and frequency_select and cycle_end_date:
                current_date = start_time.date()

                while current_date <= cycle_end_date:
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
                    else:
                        should_add = False

                    if should_add:
                        meeting = Meeting.objects.create(
                            name_pl=meeting_data["name_pl"],
                            name_en=meeting_data["name_en"],
                            start_time=datetime.combine(current_date, start_time.time()),
                            end_time=datetime.combine(current_date, end_time.time()),
                            meeting_type=meeting_data["meeting_type"],
                            room=meeting_data["room"],
                            description=meeting_data["description"],
                            color=meeting_data["color"],
                            capacity=meeting_data["capacity"],
                            is_updated=False,
                            is_approved=False,
                            event=meeting_data.get("event"),
                        )
                        # Dodajemy wykładowców do każdego utworzonego spotkania
                        if selected_lecturers:
                            meeting.lecturers.set(selected_lecturers)

                    if frequency_select in ["daily", "weekly", "biweekly", "custom_days"]:
                        current_date += timedelta(days=1)
                    elif frequency_select == "monthly":
                        next_month = (current_date.month % 12) + 1
                        current_date = current_date.replace(month=next_month)

            else:
                # Single meeting
                meeting = form.save(commit=False)
                meeting.is_approved = False
                meeting.save()
                form.save_m2m()

            return redirect("home")
    else:
        form = MeetingForm()

        form.fields["event"].queryset = events

    return render(
        request,
        "pages/calendar/new_meeting.html",
        {"form": form, "rooms": rooms, "events": events, "lecturers": lecturers},
    )


@login_required
def edit_meeting(request, meeting_id):
    # Pobierz obiekt spotkania dla zalogowanego użytkownika
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    rooms = Room.objects.all()
    events = Event.objects.all()
    lecturers = Lecturers.objects.all()

    if request.method == "POST":
        # Przekaż dane z formularza oraz instancję spotkania
        form = EditMeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            # Po zapisaniu przekieruj do "Moje Rezerwacje"
            return redirect("my_reservations")
        else:
            print(form.errors)
    else:
        # Przy pierwszym załadowaniu formularza wypełnij go istniejącymi danymi
        form = EditMeetingForm(instance=meeting)

    # Renderuj stronę edycji z formularzem
    return render(
        request,
        "pages/calendar/edit_meeting.html",
        {
            "form": form,
            "meeting": meeting,
            "rooms": rooms,
            "lecturers": lecturers,
            "events": events,
        },
    )


def new_event(request):
    lecturers = Lecturers.objects.all()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EventForm()
    return render(request, "pages/calendar/new_event.html", {"form": form, "lecturers": lecturers})


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

        meeting_filters = Q(is_approved=True)  # Ensure only approved meetings are fetched
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
