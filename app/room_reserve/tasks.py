from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_task
from room_reserve.models import Notification, User, Meeting
from room_reserve.handlers.UAMApiRoom import UAMApiHandler as RoomHandler
from room_reserve.handlers.UAMApiMeeting import UAMApiHandler as MeetingHandler
from room_reserve.handlers.UAMApiEquipment import UAMApiHandler as EquipmentHandler
from room_reserve.notifications import notify_user, notify_meeting_reminder, email_meeting_reminder
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


@task()
def send_scheduled_email(user_email, meeting_name, start_time, end_time):
    try:
        subject = f"Room Reserve - Przypomnienie o spotkaniu"
        message = (
            f'Przypomnienie o spotkaniu "{meeting_name}", które odbędzie się '
            f"od {start_time.strftime('%Y-%m-%d %H:%M')} do {end_time.strftime('%Y-%m-%d %H:%M')}."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email="powiadomienia@roomreserveuam.pl",
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"E-mail został wysłany pomyślnie do {user_email}.")
    except Exception as e:
        logger.error(f"Błąd podczas wysyłania e-maila do {user_email}: {e}")


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


@periodic_task(crontab(minute="*/10"))  # This runs every 10 minutes
def update_meeting_and_room_data():
    meeting_ids = [
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

    room_ids = [
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

    try:
        # Initialize the handler and execute the main process
        handler = MeetingHandler(meeting_ids=meeting_ids, room_ids=room_ids)
        handler.main()  # Run the main handler
    except Exception as e:
        logger.error(f"An error occurred while updating meeting and room data: {e}")


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


# email przed meetingiem


@periodic_task(crontab(minute="*/10"))  # Co minutę sprawdzaj spotkania
def schedule_meeting_notifications():

    for meeting in Meeting.objects.filter(start_time__gt=now(), is_canceled=False):
        # Zaplanuj powiadomienie 30 minut przed
        if meeting.start_time - timedelta(minutes=30) > now():
            notify_meeting_reminder.schedule((meeting.id,), eta=meeting.start_time - timedelta(minutes=30))

        # Zaplanuj e-mail
        email_meeting_reminder.schedule((meeting.id,), eta=meeting.start_time)
