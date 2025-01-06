from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


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
    first_name = models.CharField(_("First Name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, null=True, blank=True)
    department = models.CharField(_("Department"), max_length=100, null=True, blank=True)

    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        null=False,
        blank=False,
    )

    USER_TYPE_CHOICES = [
        (STUDENT, _("Student")),
        (ADMIN, _("Admin")),
        (LECTURER, _("Lecturer")),
        (GUEST, _("Guest")),
        (ORGANIZER, _("Organizer")),
    ]

    user_type = models.CharField(_("User Type"), max_length=50, choices=USER_TYPE_CHOICES, default=GUEST)

    def is_staff(self):
        # Użytkownik ma status staff, jeśli jest ADMIN lub superuser
        return self.user_type == self.ADMIN or self.is_superuser

    def is_superuser(self):
        # Django superuser ma zawsze pełne uprawnienia
        return self.is_superuser

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
        ]
