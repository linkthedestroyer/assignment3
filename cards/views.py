from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from models.models import Card


# Create your views here.
class CardSearchResultsView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "cards/card_search_results.html"

    def get_queryset(self):  # new
        card_name = self.request.GET.get("name")
        card_status = self.request.GET.get("status")
        card_rarity = self.request.GET.get("rarity")
        card_set = self.request.GET.get("set")
        card_cost = self.request.GET.get("cost")
        card_color = self.request.GET.get("color")
        card_type = self.request.GET.get("type")
        card_text = self.request.GET.get("text")

        how = self.request.GET.get("how")

        if how == 'scryfall':
            pass

        object_list = Card.objects.all()

        if card_name:
            object_list = object_list.filter(Q(card_name__icontains=card_name))
        if card_status:
            object_list = object_list.filter(Q(card_status__icontains=card_status))
        if card_rarity:
            object_list = object_list.filter(Q(card_rarity__icontains=card_rarity))
        if card_set:
            object_list = object_list.filter(Q(card_set__icontains=card_set))
        if card_cost:
            object_list = object_list.filter(Q(card_cost__icontains=card_cost))
        if card_color:
            object_list = object_list.filter(Q(card_color__icontains=card_color))
        if card_type:
            object_list = object_list.filter(Q(card_type__icontains=card_type))
        if card_text:
            object_list = object_list.filter(Q(card_text__icontains=card_text))
        if how == 'private_inventory':
            object_list = object_list.filter(Q(inventory__inventory_view_status='PRIVATE'))
        else:
            object_list = object_list.filter(Q(inventory__inventory_view_status='PUBLIC'))
        return object_list
