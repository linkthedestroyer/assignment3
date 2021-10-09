from django.contrib.auth.models import AbstractUser
from django.db import models


class MagicUser(AbstractUser):
    phone_number = models.CharField(max_length=11, default="", null=False, blank=True)

    def __str__(self):
        return "{}".format(self.username)


