from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import models as model_forms
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import CreateView, ListView
from models.models import *


class Loan_Request_Wrapper(Loan_Request):
    not_saved_loaned_cards: set[Loaned_Card] = set()


# Create your views here.
class CreateLoanRequestsView(LoginRequiredMixin, CreateView):
    model = Loan_Request
    template_name = "loan/create_loan_request.html"
    loanee_inventory: Loaned_Inventory = None

    def __new__(mcs):
        new_class = super().__new__(mcs)
        return new_class

    def get_form_class(self):
        return model_forms.modelform_factory(Loan_Request, fields=["requestor"])

    def get_object(self):
        user = self.request.user
        card_ids = eval(self.request.GET.get("ids"))
        cards: list[Card] = []
        inventories: set[Inventory] = set()
        loan_requests: list[Loan_Request] = []
        for card_id in card_ids:
            card = Card.objects.get(pk=card_id)
            cards.append(card)
            inventories.add(card.inventory)
        loanee_inventory: Loaned_Inventory = None
        if user.loaned_inventory != None:
            loanee_inventory = user.loaned_inventory
        else:
            loanee_inventory = Loaned_Inventory()
            loanee_inventory.loaned_inventory_name = "{}'s Loaned Inventory".format(user.username)

        for inventory in inventories:
            loan_request = Loan_Request()
            loan_requests.append(loan_request)
            loan_request.requestor = user
            loan_request.loaner_inventory = inventory
            loan_request.loanee_inventory = loanee_inventory
            loan_request.loan_request_status = "REQUESTED"

            loaned_card_set: set[Loaned_Card] = set()
            counter = 1
            for card in cards:
                if card.inventory.pk == inventory.pk:
                    loaned_card = Loaned_Card()
                    loaned_card.pk = counter
                    counter += 1
                    loaned_card.card = card
                    loaned_card.loan_request = loan_request
                    loaned_card_set.add(loaned_card)
            loan_request.__class__ = Loan_Request_Wrapper
            loan_request.not_saved_loaned_cards = loaned_card_set
        self.loanee_inventory = loanee_inventory
        return loan_requests

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context["request_list"] = self.get_object()
        context["loanee_inventory"] = self.loanee_inventory
        return context

    def post(self, request: HttpRequest):
        user = self.request.user
        loanee_inventory: Loaned_Inventory = None
        if user.loaned_inventory != None:
            loanee_inventory = user.loaned_inventory
        else:
            loanee_inventory = Loaned_Inventory()

        loanee_inventory.loaned_inventory_name = request.POST.get("loaned_inventory_name")
        loanee_inventory.loaned_inventory_view_status = request.POST.get("loaned_inventory_view_status")

        loanee_inventory.save()

        counter = 1
        while True == True:
            requestor_id = request.POST.get("{}-requestor_id".format(counter))
            loaner_inventory_id = request.POST.get("{}-loaner_inventory_id".format(counter))
            loanee_inventory_id = request.POST.get("{}-loanee_inventory_id".format(counter))
            if not (requestor_id == None or loaner_inventory_id == None or loanee_inventory_id == None):
                loan_request = Loan_Request()
                loan_request.requestor_id = requestor_id
                loan_request.loaner_inventory_id = loaner_inventory_id
                loan_request.loanee_inventory_id = loanee_inventory_id
                loan_request.save()
                card_counter = 1
                while True == True:
                    card_id = request.POST.get("{}-{}-card_id".format(counter, card_counter))
                    if card_id is not None:
                        loaned_card = Loaned_Card()
                        loaned_card.loan_request = loan_request
                        loaned_card.card_id = request.POST.get("{}-{}-card_id".format(counter, card_counter))
                        loaned_card.save()
                    else:
                        break
                    card_counter += 1
            else:
                break
            counter += 1
        return HttpResponseRedirect(reverse("view_loan_request"))


class LoanRequestsListView(LoginRequiredMixin, ListView):
    model = Loan_Request
    template_name = "loan/view_loan_request.html"

    def get_queryset(self):
        your_loan_requests = list(self.request.user.loan_request_set.all())
        requests_against_you = list(self.request.user.inventory.loan_request_set.all())
        complete_list: list[Loan_Request] = your_loan_requests + requests_against_you
        for loan_request in complete_list:
            if (
                loan_request.loanee_inventory.loaned_inventory_owner.pk
                == loan_request.loaner_inventory.inventory_owner.pk
            ) or loan_request.loaned_card_set.count() == 0:
                loan_request.delete()
                complete_list.remove(loan_request)
        return complete_list

    def post(self, request: HttpRequest):
        loan_request_id_and_action = request.POST.get("loan_request_id")
        loan_request_id = loan_request_id_and_action.split("_")[0]
        action = loan_request_id_and_action.split("_")[1]
        loan_request: Loan_Request = Loan_Request.objects.get(pk=loan_request_id)
        if action == "returned":
            loan_request.loan_request_status = "RETURNED"
            for loaned_card in loan_request.loaned_card_set.all():
                loaned_card.returned_date = datetime.now()
                loaned_card.card.card_status = "UNUSED"
                loaned_card.card.save()
                loaned_card.save()
        elif action == "accept":
            loan_request.loan_request_status = "ACCEPTED"
            for loaned_card in loan_request.loaned_card_set.all():
                loaned_card.card.card_status = "LOANED_OUT"
                loaned_card.card.save()
        elif action == "decline":
            loan_request.loan_request_status = "DECLINED"
        elif action == "recall":
            loan_request.loan_request_status = "RECALLED"

        loan_request.save()
        return HttpResponseRedirect(reverse("view_loan_request"))
