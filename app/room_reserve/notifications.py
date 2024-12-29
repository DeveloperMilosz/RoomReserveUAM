from room_reserve.models import Notification, Group
from django.contrib.auth import get_user_model
from django.utils.timezone import now


def notify_user(user=None, message="", submitted_by=None, is_admin_notification=False, user_type=None):
    """
    Tworzy powiadomienie dla użytkownika lub grupy.
    """
    if is_admin_notification:
        admins = get_user_model().objects.filter(is_staff=True, is_superuser=True)
        for admin in admins:
            Notification.objects.create(user=admin, message=message, submitted_by=submitted_by)
    elif user_type:
        users = get_user_model().objects.filter(user_type=user_type)
        for user in users:
            Notification.objects.create(user=user, message=message, submitted_by=submitted_by, user_type=user_type)
    elif user:
        Notification.objects.create(user=user, message=message, submitted_by=submitted_by)


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
