from room_reserve.models import Notification, Group
from django.contrib.auth import get_user_model


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


def notify_group(group, message, submitted_by=None):
    """
    Wysyła powiadomienia do wszystkich członków danej grupy.
    """
    for member in group.members.all():
        Notification.objects.create(user=member, message=message, submitted_by=submitted_by)


# Powiadomienia ogólne
def notify_test(user, submitted_by=None):
    """
    Testowe powiadomienie.
    """
    message = "This is a test notification to check the notification system."
    notify_user(user, message, submitted_by=submitted_by)


# Powiadomienia związane z rezerwacją spotkań
def notify_meeting_submission(user, meeting_name, submitted_by=None):
    """
    Powiadomienie o złożeniu wniosku o spotkanie.
    """
    message = f"Twój wniosek o spotkanie '{meeting_name}' został złożony i oczekuje na zatwierdzenie."
    notify_user(user, message, submitted_by=submitted_by)


def notify_meeting_approval(user, meeting_name, approved_by=None):
    """
    Powiadomienie o zatwierdzeniu spotkania.
    """
    message = f"Twoje spotkanie '{meeting_name}' zostało zatwierdzone przez administratora."
    notify_user(user, message, submitted_by=approved_by)


def notify_meeting_rejection(user, meeting_name, rejected_by=None):
    """
    Powiadomienie o odrzuceniu spotkania.
    """
    message = f"Twój wniosek o spotkanie '{meeting_name}' został odrzucony."
    notify_user(user, message, submitted_by=rejected_by)


# Powiadomienia dla administratorów
def notify_admin_new_meeting(meeting_name, submitted_by):
    """
    Powiadomienie do administratora o nowym wniosku o spotkanie.
    """
    message = f"Nowy wniosek o spotkanie '{meeting_name}' został złożony przez {submitted_by.username}."
    notify_user(None, message, submitted_by=submitted_by, is_admin_notification=True)


# Powiadomienia związane z wydarzeniami
def notify_event_submission(user, event_name, submitted_by=None):
    """
    Powiadomienie o złożeniu wniosku o wydarzenie.
    """
    message = f"Twój wniosek o wydarzenie '{event_name}' został złożony i oczekuje na zatwierdzenie."
    notify_user(user, message, submitted_by=submitted_by)


def notify_event_approval(user, event_name, approved_by=None):
    """
    Powiadomienie o zatwierdzeniu wydarzenia.
    """
    message = f"Twoje wydarzenie '{event_name}' zostało zatwierdzone przez administratora."
    notify_user(user, message, submitted_by=approved_by)


def notify_event_rejection(user, event_name, rejected_by=None):
    """
    Powiadomienie o odrzuceniu wydarzenia.
    """
    message = f"Twój wniosek o wydarzenie '{event_name}' został odrzucony."
    notify_user(user, message, submitted_by=rejected_by)


# Powiadomienia systemowe
def notify_custom_message(user, message, submitted_by=None):
    """
    Powiadomienie z własnym komunikatem.
    """
    notify_user(user, message, submitted_by=submitted_by)


def notify_event_submission_with_meetings(event_name, user):
    """
    Tworzy powiadomienia dla każdego administratora o nowym wydarzeniu ze spotkaniami.
    """
    user_full_name = f"{user.first_name} {user.last_name}"
    message = (
        f"Złożono wniosek o rezerwację wydarzenia '{event_name}' ze spotkaniami "
        f'przez użytkownika "{user_full_name}".'
    )
    User = get_user_model()
    admins = User.objects.filter(is_staff=True, is_superuser=True)
    for admin in admins:
        Notification.objects.create(
            user=admin,
            message=message,
            is_admin_notification=True,
            submitted_by=user,
        )
