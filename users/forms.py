from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Magic_User


class MagicUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Magic_User
        fields = ("username", "email", "phone_number")


class MagicUserChangeForm(UserChangeForm):
    class Meta:
        model = Magic_User
        fields = ("username", "email", "phone_number")
