from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_blocked = models.BooleanField(default=False)  # Campo para bloquear la cuenta
