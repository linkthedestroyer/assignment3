from django.contrib import admin

from .models import Card, Inventory, Loan_Request, Loaned_Card, Loaned_Inventory


class InventoryAdmin(admin.ModelAdmin):
    model = Inventory
    list_display = ["inventory_name", "inventory_owner", "inventory_view_status"]


class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = [
        "card_name",
        "card_status",
        "card_set",
        "card_set",
        "card_cost",
        "card_color",
        "card_type",
        "card_text",
        "inventory",
    ]


class Loaned_InventoryAdmin(admin.ModelAdmin):
    model = Loaned_Inventory
    list_display = ["loaned_inventory_name", "loaned_inventory_owner", "loaned_inventory_view_status"]


class Loan_RequestAdmin(admin.ModelAdmin):
    model = Loan_Request
    list_display = ["requestor", "loaner_inventory", "loanee_inventory", "loan_request_status"]


class Loaned_CardAdmin(admin.ModelAdmin):
    model = Loaned_Card
    list_display = ["card", "inventory", "loan_request", "loaned_inventory", "returned_date"]


# Register your models here.
admin.site.register(Card, CardAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Loan_Request, Loan_RequestAdmin)
admin.site.register(Loaned_Inventory, Loaned_InventoryAdmin)
admin.site.register(Loaned_Card, Loaned_CardAdmin)
