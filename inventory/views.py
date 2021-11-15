from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import View
from models.models import *


class CardWrapper(Card):
    count: int = 1


class InventoryWrapper(Inventory):
    consolidated_cards = []


def get_id(card_wrapper: CardWrapper):
    return card_wrapper.id


def card_in_list(card: Card, consolidated_cards):
    for consolidated_card in consolidated_cards:
        if (
            card.card_name == consolidated_card.card_name
            and card.card_color == consolidated_card.card_color
            and card.card_cost == consolidated_card.card_cost
        ):
            return consolidated_card
    return None


class UserInventoryView(LoginRequiredMixin, DetailView):
    template_name = "inventory/user_inventory.html"
    context_object_name = "user"
    model = Inventory

    def get_object(self):
        return self.request.user

    def post(self, request: HttpRequest):
        card_id = request.POST.get("card_id")
        card: Card = Card.objects.get(pk=card_id)
        card.delete()
        return HttpResponseRedirect(reverse("user_inventory"))


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
        return user.inventory

    def get_success_url(self):
        return reverse("user_inventory")


class LoanedInventoryForm(forms.ModelForm):
    class Meta:
        model = Loaned_Inventory
        fields = (
            "loaned_inventory_name",
            "loaned_inventory_view_status",
        )


class UpdateLoanedInventoryView(LoginRequiredMixin, UpdateView):
    model = Loaned_Inventory
    template_name = "inventory/edit_user_inventory.html"
    form_class = LoanedInventoryForm

    def get_object(self):
        return self.request.user.loaned_inventory

    def get_success_url(self):
        return reverse("user_inventory")


class InventoryCountWrapper(Inventory):
    total_card_count = 0
    unused_count = 0
    in_deck_count = 0
    available_for_loan_count = 0
    loaned_count = 0


class LoanedInventoryCountWrapper(Loaned_Inventory):
    total_card_count = 0


class PublicInventoryListView(TemplateView):
    model = Inventory
    template_name = "inventory/public_inventory_list.html"

    def get_inventory_set(self):
        list = Inventory.objects.filter(inventory_view_status="PUBLIC").filter(
            ~Q(inventory_owner_id=self.request.user.pk)
        )
        data_list = []
        for inventory in list:
            decorated = InventoryCountWrapper()
            data_list.append(decorated)
            decorated.pk = inventory.pk
            decorated.inventory_name = inventory.inventory_name
            decorated.inventory_owner = inventory.inventory_owner
            decorated.total_card_count = 0
            decorated.unused_count = 0
            decorated.in_deck_count = 0
            decorated.available_for_loan_count = 0
            decorated.loaned_count = 0
            for card in inventory.card_set.all():
                decorated.total_card_count += 1
                if card.card_status == "UNUSED":
                    decorated.unused_count += 1
                if card.card_status == "IN_DECK":
                    decorated.in_deck_count += 1
                if card.card_status == "AVAILABLE_FOR_LOAN":
                    decorated.available_for_loan_count += 1
                if card.card_status == "LOANED_OUT":
                    decorated.loaned_count += 1
        return data_list

    def get_loaned_set(self):
        list = Loaned_Inventory.objects.filter(loaned_inventory_view_status="PUBLIC").filter(
            ~Q(loaned_inventory_owner_id=self.request.user.pk)
        )
        data_list = []
        for loaned_inventory in list:
            decorated = LoanedInventoryCountWrapper()
            data_list.append(decorated)
            decorated.pk = loaned_inventory.pk
            decorated.loaned_inventory_name = loaned_inventory.loaned_inventory_name
            decorated.loaned_inventory_owner = loaned_inventory.loaned_inventory_owner
            decorated.total_card_count = 0
            for loan_request in loaned_inventory.loan_request_set.all():
                decorated.total_card_count += loan_request.loaned_card_set.count()
        return data_list

    def get_context_data(self, **kwargs: any):
        context = super().get_context_data(**kwargs)
        context['inventory_set'] = self.get_inventory_set()
        context['loaned_set'] = self.get_loaned_set()
        return context
