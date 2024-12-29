from django.shortcuts import render
from room_reserve.models import Notification, Group
from django.db.models import Q


def notification_history(request):
    # Oznaczanie powiadomień jako przeczytane
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

    # Pobieranie parametrów filtrowania
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    search_name = request.GET.get("search_name")
    selected_group = request.GET.get("group")
    notification_type = request.GET.get("type")

    # Filtrowanie powiadomień
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")

    if start_date and end_date:
        notifications = notifications.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

    if search_name:
        notifications = notifications.filter(Q(message__icontains=search_name))

    if selected_group:
        notifications = notifications.filter(user__group_memberships__id=selected_group)

    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)

    groups = Group.objects.all()

    return render(
        request,
        "notifications/notification_history.html",
        {
            "notifications": notifications,
            "start_date": start_date,
            "end_date": end_date,
            "search_name": search_name,
            "groups": groups,
            "selected_group": selected_group,
        },
    )
