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
    ]

    user_type = models.CharField(_("User Type"), max_length=50, choices=USER_TYPE_CHOICES, default=STUDENT)
