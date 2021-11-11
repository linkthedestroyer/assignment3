from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from models.models import *


class CardWrapper(Card):
    count: int = 1


class InventoryWrapper(Inventory):
    consolidated_cards = []


def get_id(card_wrapper: CardWrapper):
    return card_wrapper.id

def card_in_list(card: Card, consolidated_cards):
    for consolidated_card in consolidated_cards:
        if (card.card_name == consolidated_card.card_name and card.card_color == consolidated_card.card_color and card.card_cost == consolidated_card.card_cost):
            return consolidated_card
    return None

# Create your views here.
class UserInventoryView(LoginRequiredMixin, DetailView):
    template_name = "inventory/user_inventory.html"
    context_object_name = "user_inventory"
    model = Inventory

    def get_object(self):
        user = self.request.user
        test = user.inventory_set
        inventory: Inventory = test.first()
        inventory.__class__ = InventoryWrapper
        inventory.consolidated_cards = []
        cards = inventory.card_set.all()
        for card in cards:
            if card_in_list(card, inventory.consolidated_cards) != None:
                card_in_list(card, inventory.consolidated_cards).count += 1
            else:
                card.__class__ = CardWrapper
                card.count = 1
                inventory.consolidated_cards.append(card)
        return inventory


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
        return reverse("user_inventory")
