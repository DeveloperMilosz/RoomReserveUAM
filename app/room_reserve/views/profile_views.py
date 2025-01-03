from django.http import HttpResponseForbidden
from room_reserve.models import Meeting, Event, Notification
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.contrib.auth import get_user_model
from room_reserve.notifications import notify_account_type_request


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


def terms_conditions_view(request):
    return render(request, "pages/profile/regulamin.html")


User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "department"]


class UserTypeRequestForm(forms.Form):
    user_type_choices = [
        ("Student", "Student"),
        ("Lecturer", "Wykładowca"),
        ("Organizer", "Organizator"),
    ]
    requested_user_type = forms.ChoiceField(choices=user_type_choices, label="Nowy typ konta")
    reason = forms.CharField(widget=forms.Textarea, label="Powód zmiany typu konta")


@login_required
def my_profile_view(request):
    user = request.user

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, instance=user)
        type_request_form = UserTypeRequestForm(request.POST)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profil został zaktualizowany.")

        if type_request_form.is_valid():
            requested_type = type_request_form.cleaned_data["requested_user_type"]
            reason = type_request_form.cleaned_data["reason"]

            # Wysyłanie powiadomienia do administratorów
            notify_account_type_request(user, requested_type, reason)
            messages.success(request, "Twoja prośba o zmianę typu konta została wysłana.")

        return redirect("my_profile")

    else:
        profile_form = UserProfileForm(instance=user)
        type_request_form = UserTypeRequestForm()

    return render(
        request,
        "pages/profile/my_profile.html",
        {
            "profile_form": profile_form,
            "type_request_form": type_request_form,
        },
    )
