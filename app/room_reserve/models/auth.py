from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    date_joined = None
    username = models.CharField(null=True, blank=True, max_length=255)

    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        null=False,
        blank=False,
    )
