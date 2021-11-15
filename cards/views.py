import json

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import models as model_forms
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import ProcessFormView
from django.views.generic.list import ListView
from models.models import *
from users.models import Magic_User


def get_inventory_status(card: Card):
    return card.inventory.inventory_view_status


def trim(string: str):
    return string.strip()


def join(a_list: list, join: str):
    return join.join(a_list)


def get_oracle_text(card_faces):
    return card_faces["oracle_text"]


# Create your views here.
class CardSearchResultsView(LoginRequiredMixin, ListView):
    model = Card
    current_user: Magic_User = None
    has_more: bool

    def get_queryset(self):  # new
        self.has_more = False
        card_name = self.request.GET.get("name")
        card_status = self.request.GET.get("status")
        card_rarity = self.request.GET.get("rarity")
        card_set = self.request.GET.get("set")
        card_cost = self.request.GET.get("cost")
        card_color = self.request.GET.get("color")
        card_type = self.request.GET.get("type")
        card_text = self.request.GET.get("text")

        card_set_abbreviation: str = None
        card_set_name: str = None
        if card_set:
            if "_" in card_set:
                card_set_abbreviation = card_set.split("_")[0]
                card_set_name = card_set.split("_")[1]
            else:
                card_set_abbreviation = card_set
                card_set_name = card_set

        how = self.request.GET.get("how")

        if how == "scryfall":
            queryString: str = ""
            if card_name:
                card_name_array = list(map(trim, card_name.split(" ")))
                queryString = "{}".format(join(card_name_array, " and "))
            if card_rarity:
                queryString = (
                    "{} and r:{}".format(queryString, card_rarity) if queryString else "r:{}".format(card_rarity)
                )
            if card_set_abbreviation:
                queryString = (
                    "{} and s:{}".format(queryString, card_set_abbreviation)
                    if queryString
                    else "s:{}".format(card_set_abbreviation)
                )
            if card_cost:
                card_cost = join(list(map(trim, card_cost.split(" "))), "")
                queryString = "{} and m:{}".format(queryString, card_cost) if queryString else "m:{}".format(card_cost)
            if card_type:
                card_type_array = list(map(trim, card_type.split(" ")))
                queryString = (
                    "{} and t:{}".format(queryString, join(card_type_array, " and t:"))
                    if queryString
                    else "t:{}".format(join(card_type_array, " and t:"))
                )
            if card_text:
                card_text_array = list(map(trim, card_text.split(" ")))
                queryString = (
                    "{} and o:{}".format(queryString, join(card_text_array, " and o:"))
                    if queryString
                    else "o:{}".format(join(card_text_array, " and o:"))
                )

            params = {"q": queryString}
            response = requests.get("https://api.scryfall.com/cards/search", params=params)
            json_data = json.loads(response.text)
            self.has_more = json_data["has_more"]
            card_list: list[Card] = list()
            if json_data["object"] == "list":
                json_card_data_list = json_data["data"]
                for json_card_data in json_card_data_list:
                    try:
                        new_card = Card()
                        new_card.card_name = json_card_data["name"] if "name" in json_card_data else ""
                        new_card.card_status = "UNUSED"
                        new_card.card_rarity = json_card_data["rarity"] if "rarity" in json_card_data else ""
                        new_card.card_set = json_card_data["set_name"] if "set_name" in json_card_data else ""
                        if (
                            "layout" in json_card_data
                            and json_card_data["layout"] == "transform"
                            and "card_faces" in json_card_data
                        ):
                            front = json_card_data["card_faces"][0]
                            new_card.card_color = "".join(front["colors"]) if "colors" in front else ""
                            new_card.card_cost = front["mana_cost"] if "mana_cost" in front else ""
                            new_card.card_type = front["type_line"] if "type_line" in front else ""
                            new_card.card_text = front["oracle_text"] if "oracle_text" in front else ""
                            new_card.card_img_url = (
                                front["image_uris"]["normal"]
                                if "image_uris" in front and "normal" in front["image_uris"]
                                else ""
                            )
                        else:
                            new_card.card_color = (
                                "".join(json_card_data["colors"]) if "colors" in json_card_data else ""
                            )
                            new_card.card_cost = json_card_data["mana_cost"] if "mana_cost" in json_card_data else ""
                            new_card.card_type = json_card_data["type_line"] if "type_line" in json_card_data else ""
                            try:
                                new_card.card_text = (
                                    json_card_data["oracle_text"] if "oracle_text" in json_card_data else ""
                                )
                            except:
                                new_card.card_text = (
                                    " ".join(map(get_oracle_text, json_card_data["card_faces"]))
                                    if "card_faces" in json_card_data
                                    else ""
                                )
                            new_card.card_img_url = (
                                json_card_data["image_uris"]["normal"]
                                if "image_uris" in json_card_data and "normal" in json_card_data["image_uris"]
                                else ""
                            )
                        card_list.append(new_card)
                    except:
                        print("Could not create a card from: {}".format(json.dumps(json_card_data, indent=2)))
            return card_list

        object_list = Card.objects.all()
        if card_name:
            object_list = object_list.filter(Q(card_name__icontains=card_name))
        if card_status:
            object_list = object_list.filter(Q(card_status__icontains=card_status))
        if card_rarity:
            object_list = object_list.filter(Q(card_rarity__icontains=card_rarity))
        if card_set_name:
            object_list = object_list.filter(Q(card_set__icontains=card_set_name))
        if card_cost:
            object_list = object_list.filter(Q(card_cost__icontains=card_cost))
        if card_color:
            object_list = object_list.filter(Q(card_color__icontains=card_color))
        if card_type:
            object_list = object_list.filter(Q(card_type__icontains=card_type))
        if card_text:
            object_list = object_list.filter(Q(card_text__icontains=card_text))
        if how == "private_inventory":
            object_list = object_list.filter(Q(inventory__inventory_view_status="PRIVATE"))
        else:
            object_list = object_list.filter(Q(inventory__inventory_view_status="PUBLIC"))
        inventory_list = list(object_list)
        inventory_list.sort(key=self.sort)
        return inventory_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Card Search Results"
        context["has_more"] = self.has_more
        return context

    def sort(self, card: Card):
        if card.inventory.inventory_owner.pk == self.request.user.pk:
            return float("inf")
        else:
            return card.inventory.pk

    def post(self, request: HttpRequest):
        counter = 0
        inventory = request.user.inventory
        while True == True:
            if "{}_card_name".format(counter) not in request.POST:
                break
            card = Card()
            card.card_name = request.POST.get("{}_card_name".format(counter))
            card.card_status = "UNUSED"
            card.card_rarity = request.POST.get("{}_card_rarity".format(counter))
            card.card_set = request.POST.get("{}_card_set".format(counter))
            card.card_cost = request.POST.get("{}_card_cost".format(counter))
            card.card_color = request.POST.get("{}_card_color".format(counter))
            card.card_type = request.POST.get("{}_card_type".format(counter))
            card.card_text = request.POST.get("{}_card_text".format(counter))
            card.card_img_url = request.POST.get("{}_card_img_url".format(counter))
            card.inventory = inventory
            card.save()
            counter += 1
        return HttpResponseRedirect(reverse("user_inventory"))


class CardViewer(LoginRequiredMixin, ListView):
    model = Card
    template_name = "cards/internal_card_search_results.html"
    current_user: Magic_User = None
    title: str

    def get_queryset(self):
        # This will be something like Loan_Request or Loaned_Inventory or Inventory
        requester_type = self.request.GET.get("requester_type")
        requester_id = self.request.GET.get("requester_id")

        data = eval(requester_type).objects.get(pk=requester_id)

        cards = []

        if requester_type == "Loan_Request":
            self.title = "{}'s loan request".format(data.requestor.username)
            for loaned_card in data.loaned_card_set.all():
                cards.append(loaned_card.card)
        elif requester_type == "Loaned_Inventory":
            self.title = "Loaned inventory: {}".format(data.loaned_inventory_name)
            for loan_request in data.loan_request_set.all():
                for loaned_card in loan_request.loaned_card_set.all():
                    cards.append(loaned_card.card)
        elif requester_type == "Inventory":
            self.title = "Inventory: {}".format(data.inventory_name)
            for card in data.card_set.all():
                cards.append(card)
        return cards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context
