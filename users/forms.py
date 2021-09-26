from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import MagicUser


class MagicUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = MagicUser
        fields = ("username", "email", "phone_number")


class MagicUserChangeForm(UserChangeForm):
    class Meta:
        model = MagicUser
        fields = ("username", "email", "phone_number")
