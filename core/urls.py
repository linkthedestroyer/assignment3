from cards.views import *
from django.urls import path
from django.views.generic.base import TemplateView
from inventory.views import *
from loans.views import *

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("inventory/", UserInventoryView.as_view(), name="user_inventory"),
    path("inventory/edit", UpdateUserInventoryView.as_view(), name="edit_user_inventory"),
    path("inventory/loaned/edit", UpdateLoanedInventoryView.as_view(), name="edit_loaned_inventory"),
    path("inventory/list/public", PublicInventoryListView.as_view(), name="public_inventory_list"),
    path(
        "card/search",
        TemplateView.as_view(template_name="cards/card_search.html"),
        name="card_search",
    ),
    path(
        "card/search/internal/results",
        CardSearchResultsView.as_view(template_name="cards/internal_card_search_results.html"),
        name="internal_card_search_results",
    ),
    path(
        "card/search/external/results",
        CardSearchResultsView.as_view(template_name="cards/external_card_search_results.html"),
        name="external_card_search_results",
    ),
    path("card/view", CardViewer.as_view(), name="card_view"),
    path(
        "loan/create/request",
        CreateLoanRequestsView.as_view(),
        name="create_loan_request",
    ),
    path(
        "loan/view/requests",
        LoanRequestsListView.as_view(),
        name="view_loan_request",
    ),
]
