from django.shortcuts import render
from room_reserve.models import Notification


def notification_history(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/notification_history.html", {"notifications": notifications})
