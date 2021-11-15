from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import CreateView

from users.forms import MagicUserCreationForm
from users.models import Magic_User

# Create your views here.


class CreateMagicUserView(CreateView):
    model = Magic_User
    template_name = "user/create_user.html"
    form_class = MagicUserCreationForm

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        else:
            return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse("login") + "?success='true'"
