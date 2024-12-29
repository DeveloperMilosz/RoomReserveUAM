from huey import crontab
from huey.contrib.djhuey import periodic_task, task
from room_reserve.models import Notification, User
from room_reserve.handlers.UAMApiRoom import UAMApiHandler as RoomHandler
from room_reserve.handlers.UAMApiMeeting import UAMApiHandler as MeetingHandler
from room_reserve.handlers.UAMApiEquipment import UAMApiHandler as EquipmentHandler
from room_reserve.notifications import notify_user
from django.core.mail import send_mail


@task()
def send_notification_task(user_id=None, message="", submitted_by=None, user_type=None):
    """
    Wysyła powiadomienia asynchronicznie.
    """
    if user_id:
        user = User.objects.get(id=user_id)
        notify_user(user=user, message=message, submitted_by=submitted_by)
    elif user_type:
        notify_user(message=message, submitted_by=submitted_by, user_type=user_type)


@periodic_task(crontab(hour="0", minute="0"))  # Uruchamiane codziennie o północy
def send_daily_notification_email():
    users_with_notifications = User.objects.filter(notifications__is_read=False).distinct()

    for user in users_with_notifications:
        unread_count = user.notifications.filter(is_read=False).count()
        send_mail(
            subject="Masz nowe powiadomienia w aplikacji Room Reserve",
            message=f"Masz {unread_count} nowych powiadomień. Zaloguj się do aplikacji, aby je zobaczyć.",
            from_email="powiadomienia@roomreserveuam.pl",
            recipient_list=[user.email],
        )


# Zadanie do pobierania danych o pokojach co 10 minut
@periodic_task(crontab(minute="*/10"))  # Uruchamiane co 10 minut
def update_room_data():
    handler = RoomHandler(
        room_ids=[
            2488,
            2489,
            2490,
            2684,
            2685,
            2686,
            2687,
            2688,
            2689,
            2690,
            2691,
            2692,
            2693,
            2694,
            2695,
            2696,
            2697,
            2698,
            2699,
            2700,
            2701,
            2702,
            2703,
            2777,
        ]
    )
    handler.main()  # Wywołaj metodę główną do pobrania i zapisania danych


# Zadanie do pobierania danych o spotkaniach co 10 minut
@periodic_task(crontab(minute="*/10"))  # Uruchamiane co 10 minut
def update_meeting_data():
    handler = MeetingHandler(
        meeting_ids=[
            2488,
            2489,
            2490,
            2684,
            2685,
            2686,
            2687,
            2688,
            2689,
            2690,
            2691,
            2692,
            2693,
            2694,
            2695,
            2696,
            2697,
            2698,
            2699,
            2700,
            2701,
            2702,
            2703,
            2704,
            2777,
        ]
    )
    handler.main()  # Wywołaj metodę główną do pobrania i zapisania danych


@periodic_task(crontab(minute="*/10"))  # Uruchamiane co 10 minut
def update_equipment_data():
    handler = EquipmentHandler(
        room_ids=[
            2488,
            2489,
            2490,
            2684,
            2685,
            2686,
            2687,
            2688,
            2689,
            2690,
            2691,
            2692,
            2693,
            2694,
            2695,
            2696,
            2697,
            2698,
            2699,
            2700,
            2701,
            2702,
            2703,
            2777,
        ]
    )
    handler.main()  # Wywołaj metodę główną do pobrania i zapisania danych
