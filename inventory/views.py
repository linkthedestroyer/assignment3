from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from models.models import *


# Create your views here.
class UserInventoryView(LoginRequiredMixin, DetailView):
    template_name = "inventory/user_inventory.html"
    context_object_name = 'user_inventory'
    model = Inventory

    def get_object(self):
        user = self.request.user
        test = user.inventory_set
        return test.first()


class UserInventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = (
            "inventory_name",
            "inventory_view_status",
        )



class UpdateUserInventoryView(LoginRequiredMixin, UpdateView):
    model = Inventory
    template_name = "inventory/edit_user_inventory.html"
    form_class = UserInventoryForm

    def get_object(self):
        user = self.request.user
        test = user.inventory_set
        return test.first()


    def get_success_url(self):
        return reverse('user_inventory')
