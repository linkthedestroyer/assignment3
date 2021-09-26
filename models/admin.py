from django.contrib import admin

from .models import (Card, Inventory, Loan_Request, Loaned_Card,
                     Loaned_Inventory, Loanee, Loaner)


class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = [
        "card_name",
        "inventory",
    ]


class InventoryAdmin(admin.ModelAdmin):
    model = Inventory
    list_display = [
        "inventory_name",
        "inventory_owner",
    ]


class LoaneeAdmin(admin.ModelAdmin):
    model = Loanee
    list_display = ["user"]


class LoanerAdmin(admin.ModelAdmin):
    model = Loaner
    list_display = ["user"]


class Loan_RequestAdmin(admin.ModelAdmin):
    model = Loan_Request
    list_display = ["requestor_user", "loaner_user"]


class Loaned_CardAdmin(admin.ModelAdmin):
    model = Loaned_Card
    list_display = ["card", "inventory", "loaned_inventory"]


class Loaned_InventoryAdmin(admin.ModelAdmin):
    model = Loaned_Inventory
    list_display = ["loaned_inventory_name", "loaned_inventory_loanee_user", "loaned_inventory_loaner_user"]


# Register your models here.
admin.site.register(Card, CardAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Loanee, LoaneeAdmin)
admin.site.register(Loaner, LoanerAdmin)
admin.site.register(Loan_Request, Loan_RequestAdmin)
admin.site.register(Loaned_Inventory, Loaned_InventoryAdmin)
admin.site.register(Loaned_Card, Loaned_CardAdmin)
