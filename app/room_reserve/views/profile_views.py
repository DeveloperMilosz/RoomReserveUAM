from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from room_reserve.models import Meeting


@login_required
def my_profile_view(request):
    return render(request, "pages/profile/my_profile.html")


@login_required
def my_reservations(request):
    user = request.user

    # Filtruj rezerwacje użytkownika
    pending_reservations = Meeting.objects.filter(submitted_by=user, is_approved=False)
    approved_reservations = Meeting.objects.filter(submitted_by=user, is_approved=True)
    rejected_reservations = Meeting.objects.filter(submitted_by=user).exclude(is_approved=True, is_updated=True)

    return render(
        request,
        "pages/profile/my_reservations.html",
        {
            "pending_reservations": pending_reservations,
            "approved_reservations": approved_reservations,
            "rejected_reservations": rejected_reservations,
        },
    )
