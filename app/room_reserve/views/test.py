from django.shortcuts import render, redirect
from django.core.mail import send_mail
from room_reserve.models import User
from room_reserve.notifications import notify_user


def test_notifications(request):
    if request.method == "POST":
        user_id = request.POST.get("user")  # Pobieramy ID wybranego użytkownika
        message = request.POST.get("message")
        email_subject = request.POST.get("email_subject")
        email_content = request.POST.get("email_content")
        send_email = "send_email" in request.POST  # Czy zaznaczono wysyłanie e-maila

        # Sprawdzenie, czy wybrano użytkownika
        if not user_id:
            return render(
                request,
                "test_notification.html",
                {
                    "error": "Musisz wybrać użytkownika.",
                    "users": User.objects.all(),
                },
            )

        # Znalezienie użytkownika
        user = User.objects.get(id=user_id)

        # Tworzenie powiadomienia
        notify_user(user=user, message=message, submitted_by=request.user)

        # Wysyłanie e-maila, jeśli zaznaczono opcję
        if send_email:
            send_mail(
                subject=email_subject or "Powiadomienie od Room Reserve",
                message=email_content or message,
                from_email="powiadomienia@roomreserveuam.pl",
                recipient_list=[user.email],
            )

        return redirect("test_notification")  # Po wysłaniu przekierowanie na tę samą stronę

    return render(
        request,
        "test_notification.html",
        {
            "users": User.objects.all(),
        },
    )
