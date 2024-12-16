from django.shortcuts import render, redirect
from room_reserve.models import Group, User
from room_reserve.notifications import notify_user, notify_group


def test_notifications(request):
    if request.method == "POST":
        user_id = request.POST.get("user")
        group_id = request.POST.get("group")
        message = request.POST.get("message")

        # Walidacja: tylko użytkownik LUB grupa mogą być wybrane
        if user_id and group_id:
            return render(
                request,
                "test_notification.html",
                {
                    "error": "Możesz wybrać tylko użytkownika ALBO grupę.",
                    "users": User.objects.all(),
                    "groups": Group.objects.all(),
                },
            )

        if user_id:
            user = User.objects.get(id=user_id)
            notify_user(user=user, message=message, submitted_by=request.user)
        elif group_id:
            group = Group.objects.get(id=group_id)
            notify_group(group=group, message=message, submitted_by=request.user)
        else:
            return render(
                request,
                "test_notification.html",
                {
                    "error": "Musisz wybrać użytkownika lub grupę.",
                    "users": User.objects.all(),
                    "groups": Group.objects.all(),
                },
            )

        return redirect("test_notification")  # Po wysłaniu przekierowanie na tę samą stronę

    return render(
        request,
        "test_notification.html",
        {
            "users": User.objects.all(),
            "groups": Group.objects.all(),
        },
    )
