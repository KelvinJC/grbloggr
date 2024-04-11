from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email_address'), unique=True, db_index=True)
    phone_number = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self) -> str:
        return self.username