from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from room_reserve.models import Meeting, Event


@login_required
def my_reservations(request):
    user = request.user

    # Ograniczenie widoku do ADMIN, LECTURER i GUEST
    if user.user_type not in ["Admin", "Lecturer", "Guest"]:
        return HttpResponseForbidden("Nie masz uprawnień do przeglądania tej strony.")

    # Filtruj spotkania (Meeting) dla zalogowanego użytkownika
    pending_meetings = Meeting.objects.filter(submitted_by=user, is_approved=False, is_rejected=False)
    approved_meetings = Meeting.objects.filter(submitted_by=user, is_approved=True)
    rejected_meetings = Meeting.objects.filter(submitted_by=user, is_rejected=True)

    # Filtruj wydarzenia (Event) dla zalogowanego użytkownika
    pending_events = Event.objects.filter(submitted_by=user, is_approved=False, is_rejected=False)
    approved_events = Event.objects.filter(submitted_by=user, is_approved=True)
    rejected_events = Event.objects.filter(submitted_by=user, is_rejected=True)

    return render(
        request,
        "pages/profile/my_reservations.html",
        {
            "pending_meetings": pending_meetings,
            "approved_meetings": approved_meetings,
            "rejected_meetings": rejected_meetings,
            "pending_events": pending_events,
            "approved_events": approved_events,
            "rejected_events": rejected_events,
        },
    )


@login_required
def my_profile_view(request):
    return render(request, "pages/profile/my_profile.html")
