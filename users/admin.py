from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MagicUserChangeForm, MagicUserCreationForm
from .models import Magic_User


class MagicUserAdmin(UserAdmin):
    add_form = MagicUserCreationForm
    form = MagicUserChangeForm
    model = Magic_User
    list_display = [
        "username",
        "email",
        "phone_number",
        "is_staff",
    ]


admin.site.register(Magic_User, MagicUserAdmin)
