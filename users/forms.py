from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import Magic_User


class MagicUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Magic_User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "address")


class MagicUserChangeForm(UserChangeForm):
    class Meta:
        model = Magic_User
        fields = ("username", "email", "phone_number")
