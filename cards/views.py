from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from models.models import Card


# Create your views here.
class CardSearchResultsView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "card_search.html"

    def get_queryset(self):  # new
        card_name = self.request.GET.get("card_name")
        card_status = self.request.GET.get("card_status")
        card_rarity = self.request.GET.get("card_rarity")
        card_set = self.request.GET.get("card_set")
        card_cost = self.request.GET.get("card_cost")
        card_color = self.request.GET.get("card_color")
        card_type = self.request.GET.get("card_type")
        card_text = self.request.GET.get("card_text")

        object_list = Card.objects.filter(
            Q(card_name__icontains=card_name)
            | Q(card_status__icontains=card_status)
            | Q(card_rarity__icontains=card_rarity)
            | Q(card_set__icontains=card_set)
            | Q(card_cost__icontains=card_cost)
            | Q(card_color__icontains=card_color)
            | Q(card_type__icontains=card_type)
            | Q(card_text__icontains=card_text)
        )
        return object_list
