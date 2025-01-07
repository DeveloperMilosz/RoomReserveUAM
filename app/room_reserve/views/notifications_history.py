from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from room_reserve.models import Notification, Group
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def message_history(request):
    # Filtrowanie wiadomości
    search_email = request.GET.get("search_email", "")
    search_content = request.GET.get("search_content", "")
    group_id = request.GET.get("group", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    messages_qs = Notification.objects.filter(notification_type="message", user=request.user)

    # Dodanie filtrów
    if search_email:
        messages_qs = messages_qs.filter(submitted_by__email__icontains=search_email)
    if search_content:
        messages_qs = messages_qs.filter(message__icontains=search_content)
    if group_id:
        messages_qs = messages_qs.filter(user__group_memberships__id=group_id)
    if start_date and end_date:
        messages_qs = messages_qs.filter(created_at__range=[start_date, end_date])

    groups = Group.objects.all()

    # Obsługa formularza wysyłania powiadomień
    if request.method == "POST":
        group_ids = request.POST.getlist("groups")  # Lista grup
        emails = request.POST.get("emails")  # Lista e-maili jako string
        content = request.POST.get("content")  # Treść wiadomości

        # Walidacja treści wiadomości
        if not content.strip():
            messages.error(request, "Treść wiadomości nie może być pusta.")
            return redirect("message_history")

        # Wysyłanie do grup
        if group_ids:
            for group_id in group_ids:
                try:
                    group = Group.objects.get(id=group_id)
                    for user in group.members.all():
                        Notification.objects.create(
                            user=user, message=content, notification_type="message", submitted_by=request.user
                        )
                except Group.DoesNotExist:
                    messages.error(request, f"Grupa o ID {group_id} nie istnieje.")
                    continue

        # Wysyłanie do użytkowników przez e-mail
        if emails:
            email_list = [email.strip() for email in emails.split(",") if email.strip()]
            for email in email_list:
                try:
                    user = User.objects.get(email=email)
                    Notification.objects.create(
                        user=user, message=content, notification_type="message", submitted_by=request.user
                    )
                except User.DoesNotExist:
                    messages.error(request, f"Użytkownik o e-mailu {email} nie istnieje.")

        # Potwierdzenie sukcesu
        messages.success(request, "Powiadomienia zostały wysłane.")
        return redirect("message_history")

    return render(
        request,
        "notifications/message_history.html",
        {
            "messages": messages_qs,
            "groups": groups,
        },
    )


@login_required
def alert_history(request):
    search_content = request.GET.get("search_content", "")
    group_id = request.GET.get("group", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")

    alerts = Notification.objects.filter(notification_type="notification", user=request.user)

    if search_content:
        alerts = alerts.filter(message__icontains=search_content)
    if group_id:
        alerts = alerts.filter(user__group_memberships__id=group_id)
    if start_date and end_date:
        alerts = alerts.filter(created_at__range=[start_date, end_date])

    groups = Group.objects.all()
    return render(
        request,
        "notifications/alert_history.html",
        {
            "alerts": alerts,
            "groups": groups,
        },
    )


@login_required
def send_notification(request):
    """
    Wysyła powiadomienia typu "message" do użytkowników lub grup.
    """
    if request.method == "POST":
        group_ids = request.POST.getlist("groups")  # Lista grup
        emails = request.POST.get("emails")  # Lista e-maili jako string
        content = request.POST.get("content")  # Treść wiadomości

        # Walidacja treści wiadomości
        if not content.strip():
            messages.error(request, "Treść wiadomości nie może być pusta.")
            return redirect("send_notification")

        # Wysyłanie do grup
        if group_ids:
            for group_id in group_ids:
                try:
                    group = Group.objects.get(id=group_id)
                    for user in group.members.all():
                        Notification.objects.create(
                            user=user, message=content, notification_type="message", submitted_by=request.user
                        )
                except Group.DoesNotExist:
                    messages.error(request, f"Grupa o ID {group_id} nie istnieje.")
                    continue

        # Wysyłanie do użytkowników przez e-mail
        if emails:
            email_list = [email.strip() for email in emails.split(",") if email.strip()]
            for email in email_list:
                try:
                    user = User.objects.get(email=email)
                    Notification.objects.create(
                        user=user, message=content, notification_type="message", submitted_by=request.user
                    )
                except User.DoesNotExist:
                    messages.error(request, f"Użytkownik o e-mailu {email} nie istnieje.")

        # Potwierdzenie sukcesu
        messages.success(request, "Powiadomienia zostały wysłane.")
        return redirect("alert_history")

    groups = Group.objects.all()
    return render(
        request,
        "notifications/send_notification.html",
        {
            "groups": groups,
        },
    )


# from django.shortcuts import render
# from room_reserve.models import Notification, Group
# from django.db.models import Q


# def notification_history(request):
#     # Oznaczanie powiadomień jako przeczytane
#     if request.user.is_authenticated:
#         Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

#     # Pobieranie parametrów filtrowania
#     start_date = request.GET.get("start_date")
#     end_date = request.GET.get("end_date")
#     search_name = request.GET.get("search_name")
#     selected_group = request.GET.get("group")
#     notification_type = request.GET.get("type")

#     # Filtrowanie powiadomień
#     notifications = Notification.objects.filter(user=request.user).order_by("-created_at")

#     if start_date and end_date:
#         notifications = notifications.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

#     if search_name:
#         notifications = notifications.filter(Q(message__icontains=search_name))

#     if selected_group:
#         notifications = notifications.filter(user__group_memberships__id=selected_group)

#     if notification_type:
#         notifications = notifications.filter(notification_type=notification_type)

#     groups = Group.objects.all()

#     return render(
#         request,
#         "notifications/notification_history.html",
#         {
#             "notifications": notifications,
#             "start_date": start_date,
#             "end_date": end_date,
#             "search_name": search_name,
#             "groups": groups,
#             "selected_group": selected_group,
#         },
#     )
