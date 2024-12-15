from django.shortcuts import redirect
from room_reserve.models import Notification


def mark_notifications_as_read(request):
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect("home")
