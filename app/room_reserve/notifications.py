from room_reserve.models import Notification, Group, Meeting, User
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from huey import crontab
from huey.contrib.djhuey import task
from django.core.mail import send_mail

User = get_user_model()


def create_notification(user=None, groups=None, message="", notification_type="message"):
    """
    Tworzy powiadomienie dla wybranego użytkownika lub wielu grup.
    """
    if user:
        # Tworzenie powiadomienia dla jednego użytkownika
        Notification.objects.create(user=user, message=message, notification_type=notification_type)

    if groups:
        # Tworzenie powiadomień dla członków wielu grup
        for group in groups:
            for member in group.members.all():
                Notification.objects.create(user=member, message=message, notification_type=notification_type)


def notify_user(user=None, message="", submitted_by=None, is_admin_notification=False, user_type=None):
    """
    Tworzy powiadomienie dla użytkownika lub grupy.
    """
    if is_admin_notification:
        admins = get_user_model().objects.filter(is_staff=True, is_superuser=True)
        for admin in admins:
            Notification.objects.create(
                user=admin, message=message, submitted_by=submitted_by, notification_type="notification"
            )
    elif user_type:
        users = get_user_model().objects.filter(user_type=user_type)
        for user in users:
            Notification.objects.create(
                user=user,
                message=message,
                submitted_by=submitted_by,
                user_type=user_type,
                notification_type="notification",
            )
    elif user:
        Notification.objects.create(
            user=user, message=message, submitted_by=submitted_by, notification_type="notification"
        )


# do rezerwacji spotkania
def notify_meeting_submission(user, meeting_name, submitted_by=None):
    """
    Powiadomienie o złożeniu wniosku o spotkanie dla użytkownika.
    """
    submission_date = now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Złożyłeś wniosek o spotkanie o nazwie '{meeting_name}' w dniu {submission_date}."
    notify_user(user, message, submitted_by=submitted_by)


def notify_admin_meeting_submission(meeting_name, submitted_by):
    """
    Powiadomienie do administratorów o nowym wniosku o spotkanie.
    """
    submission_date = now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{submitted_by.first_name} {submitted_by.last_name} ({submitted_by.email})"
    message = f"Użytkownik {user_info} złożył wniosek o spotkanie '{meeting_name}' w dniu {submission_date}."
    notify_user(None, message, submitted_by=submitted_by, is_admin_notification=True)


# do rezerwacji wydarzeń
def notify_event_submission(user, event_name, submitted_by=None):
    """
    Powiadomienie o złożeniu wniosku o wydarzenie dla użytkownika.
    """
    submission_date = now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Złożyłeś wniosek o wydarzenie o nazwie '{event_name}' w dniu {submission_date}."
    notify_user(user, message, submitted_by=submitted_by)


def notify_admin_event_submission(event_name, submitted_by):
    """
    Powiadomienie do administratorów o nowym wniosku o wydarzenie.
    """
    submission_date = now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{submitted_by.first_name} {submitted_by.last_name} ({submitted_by.email})"
    message = f"Użytkownik {user_info} złożył wniosek o wydarzenie '{event_name}' w dniu {submission_date}."
    notify_user(None, message, submitted_by=submitted_by, is_admin_notification=True)


# powiadomienie o nowym wydarzeniu ze spotkaniami
def notify_event_with_meetings_submission(user, event_name, submitted_by=None):
    """
    Powiadomienie o złożeniu wniosku o wydarzenie ze spotkaniami dla użytkownika.
    """
    submission_date = now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Złożyłeś wniosek o wydarzenie ze spotkaniami o nazwie '{event_name}' w dniu {submission_date}."
    notify_user(user, message, submitted_by=submitted_by)


def notify_admin_event_with_meetings_submission(event_name, submitted_by):
    """
    Powiadomienie do administratorów o nowym wniosku o wydarzenie ze spotkaniami.
    """
    submission_date = now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"{submitted_by.first_name} {submitted_by.last_name} ({submitted_by.email})"
    message = (
        f"Użytkownik {user_info} złożył wniosek o wydarzenie ze spotkaniami '{event_name}' w dniu {submission_date}."
    )
    notify_user(None, message, submitted_by=submitted_by, is_admin_notification=True)


# powiadomieniu o prosbie o zmiane typu konta
def notify_account_type_request(user, requested_type, reason):
    """
    Tworzy powiadomienie dla wszystkich administratorów o prośbie zmiany typu konta.
    """
    message = (
        f"Użytkownik {user.first_name} {user.last_name} ({user.email}) prosi o zmianę typu konta na '{requested_type}'. "
        f"Powód: {reason}."
    )
    admins = User.objects.filter(is_staff=True, is_superuser=True)
    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=message,
            submitted_by=user,
            notification_type="notification",
        )


# powiadomienia przed spotkaniem


@task()
def notify_meeting_reminder(meeting_id):
    """
    Wysyła powiadomienie 30 minut przed spotkaniem w aplikacji.
    """
    meeting = Meeting.objects.get(id=meeting_id)
    if meeting.start_time > now():
        Notification.objects.create(
            user=meeting.submitted_by,
            message=f"Przypomnienie: Spotkanie '{meeting.name_pl}' rozpoczyna się za 30 minut.",
            notification_type="notification",
            submitted_by=None,
        )


@task()
def email_meeting_reminder(meeting_id, email_time=None):
    """
    Wysyła przypomnienie e-mail o spotkaniu.
    """
    meeting = Meeting.objects.get(id=meeting_id)
    email_time = email_time or meeting.start_time
    if email_time <= now():
        send_mail(
            subject=f"Przypomnienie o spotkaniu: {meeting.name_pl}",
            message=f"Spotkanie '{meeting.name_pl}' rozpoczyna się {meeting.start_time}.",
            from_email="powiadomienia@roomreserveuam.pl",
            recipient_list=[meeting.submitted_by.email],
        )
