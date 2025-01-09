from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.contrib.auth.models import UserManager


class DefaultUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.update(
            {
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "user_type": "Admin",
            }
        )
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    STUDENT = "Student"
    ADMIN = "Admin"
    LECTURER = "Lecturer"
    GUEST = "Guest"
    ORGANIZER = "Organizer"

    date_joined = None
    username = models.CharField(null=True, blank=True, max_length=255)
    first_name = models.CharField(_("Imie"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Nazwisko"), max_length=50, null=True, blank=True)
    department = models.CharField(_("Wydział "), max_length=100, null=True, blank=True)

    email = models.EmailField(
        verbose_name=_("Adres Email"),
        unique=True,
        null=False,
        blank=False,
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
        verbose_name="Zdjęcie Profilowe"
    )

    USER_TYPE_CHOICES = [
        (STUDENT, _("Student")),
        (ADMIN, _("Admin")),
        (LECTURER, _("Lecturer")),
        (GUEST, _("Guest")),
        (ORGANIZER, _("Organizer")),
    ]

    user_type = models.CharField(_("User Type"), max_length=50, choices=USER_TYPE_CHOICES, default=GUEST)

    objects = DefaultUserManager()


# Signals
def pre_update_user(sender, instance: User, **kwargs):
    if instance.user_type == User.ADMIN:
        instance.is_staff = True
        instance.is_superuser = True
    else:
        instance.is_staff = False
        instance.is_superuser = False


pre_save.connect(pre_update_user, sender=User)
