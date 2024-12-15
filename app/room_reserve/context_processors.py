from room_reserve.models import Notification


def notifications_processor(request):
    if request.user.is_authenticated:
        # Pobierz nieprzeczytane powiadomienia
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")[:10]
        return {"header_notifications": notifications}
    return {"header_notifications": []}
