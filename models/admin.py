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
        "card_cost",
        "card_color",
        "card_type",
        "inventory_view",
    ]

    @admin.display(empty_value='N/A', description='Inventory')
    def inventory_view(self, obj: Card):
        return '{}'.format(obj.inventory.inventory_name)


class Loaned_InventoryAdmin(admin.ModelAdmin):
    model = Loaned_Inventory
    list_display = ["loaned_inventory_name", "loaned_inventory_owner", "loaned_inventory_view_status"]


class Loan_RequestAdmin(admin.ModelAdmin):
    model = Loan_Request
    list_display = ["requestor", "loaner_inventory_view", "loanee_inventory_view", "loan_request_status"]


    @admin.display(empty_value='N/A', description='Loaner Inventory')
    def loaner_inventory_view(self, obj: Loan_Request):
        return '{}'.format(obj.loaner_inventory.inventory_name)

    @admin.display(description='Loanee Inventory')
    def loanee_inventory_view(self, obj: Loan_Request):
        if obj.loanee_inventory == None:
            return 'N/A'
        return '{}'.format(obj.loanee_inventory.loaned_inventory_name)


class Loaned_CardAdmin(admin.ModelAdmin):
    model = Loaned_Card
    list_display = ["card_view", "inventory_view", "loan_request_view", "loaned_inventory_view", "returned_date"]

    @admin.display(empty_value='N/A', description='Card')
    def card_view(self, obj: Loaned_Card):
        return '{}'.format(obj.card.card_name)

    @admin.display(empty_value='N/A', description='Inventory')
    def inventory_view(self, obj: Loaned_Card):
        return '{}'.format(obj.inventory.inventory_name)

    @admin.display(empty_value='N/A', description='Loan Request')
    def loan_request_view(self, obj: Loaned_Card):
        return 'Request by {} to {}'.format(obj.loan_request.requestor, obj.loan_request.loaner_inventory.inventory_owner)

    @admin.display(empty_value='N/A', description='Loaned Inventory')
    def loaned_inventory_view(self, obj: Loaned_Card):
        if obj.loaned_inventory == None:
            return None
        return '{}'.format(obj.loaned_inventory.loaned_inventory_name)


# Register your models here.
admin.site.register(Card, CardAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Loan_Request, Loan_RequestAdmin)
admin.site.register(Loaned_Inventory, Loaned_InventoryAdmin)
admin.site.register(Loaned_Card, Loaned_CardAdmin)
