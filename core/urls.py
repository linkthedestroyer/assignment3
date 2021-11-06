from django.urls import path
from django.views.generic.base import TemplateView

from inventory.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("inventory/", UserInventoryView.as_view(), name="user_inventory"),
    path("inventory/edit", UpdateUserInventoryView.as_view(), name="edit_user_inventory")
]
