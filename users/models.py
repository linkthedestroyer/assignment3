from django.contrib.auth.models import AbstractUser
from django.db import models


class Magic_User(AbstractUser):
    phone_number = models.CharField(max_length=11, default="", null=False, blank=True)
    address = models.CharField(max_length=100, default='', null=True, blank=True)

    def __str__(self):
        return "{}".format(self.username)
    
    def all(self):
        print(self.first_name, self.last_name, self.email, self.username, self.phone_number, self.password)


