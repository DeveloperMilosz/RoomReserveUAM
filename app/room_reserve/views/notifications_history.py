from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from room_reserve.models import Notification


@login_required
def notification_history(request):
    """
    Wyświetla historię wszystkich powiadomień użytkownika.
    """
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(notifications, 15)  # 10 powiadomień na stronę

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "notifications/notification_history.html", {"page_obj": page_obj})
