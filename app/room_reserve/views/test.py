from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from room_reserve.notifications import notify_admin_new_meeting, notify_event_approval


@login_required
def test_notify_admin(request):
    """
    Testuje wysyłanie powiadomień do administratorów.
    """
    if request.method == "POST":
        meeting_name = request.POST.get("meeting_name")
        notify_admin_new_meeting(meeting_name, submitted_by=request.user)
    return redirect("test_notifications")


@login_required
def test_notify_event_approval(request):
    """
    Testuje wysyłanie powiadomień o zatwierdzeniu wydarzenia do użytkownika.
    """
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        event_name = request.POST.get("event_name")

        try:
            user = User.objects.get(id=user_id)
            notify_event_approval(user, event_name, approved_by=request.user)
        except User.DoesNotExist:
            pass  # Możesz obsłużyć wyjątek, jeśli chcesz

    return redirect("test_notifications")


@login_required
def test_notifications(request):
    """
    Widok testowy wyświetlający powiadomienia użytkownika.
    """
    notifications = request.user.notifications.order_by("-created_at")
    return render(request, "notifications/test_notification.html", {"notifications": notifications})
