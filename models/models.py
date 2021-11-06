from django.contrib.auth import get_user, get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from users.models import Magic_User


class Inventory(models.Model):
    inventory_name = models.CharField(max_length=50, blank=False, null=False, default=" ")
    inventory_owner = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    inventory_view_status = models.CharField(
        max_length=50, blank=False, null=False, default="PUBLIC", choices=(("PUBLIC", "Public"), ("PRIVATE", "Private"))
    )

    class Meta:
        verbose_name_plural = "Inventories"

    @classmethod
    def create(cls, inventory_name, user):
        inventory = cls(inventory_name=inventory_name, inventory_owner=user)
        return inventory

    def __str__(self):
        return "Inventory=[inventory_name={},inventory_owner={},inventory_view_status={}]".format(
            self.inventory_name, self.inventory_owner, self.inventory_view_status
        )


CARD_CHOICES = (
    ("UNUSED", "Unused"),
    ("IN_DECK", "In Deck"),
    ("AVAILABLE_FOR_LOAN", "Available for Loan"),
    ("LOANED_OUT", "Loaned Out"),
)


class Card(models.Model):
    card_name = models.CharField(max_length=50, blank=False, null=False, default=" ")
    card_status = models.CharField(max_length=50, blank=False, null=False, default="UNUSED", choices=CARD_CHOICES)
    card_rarity = models.CharField(max_length=20, blank=False, null=False, default=" ")
    card_set = models.CharField(max_length=20, blank=False, null=False, default=" ")
    card_cost = models.CharField(max_length=20, blank=False, null=False, default=" ")
    card_color = models.CharField(max_length=20, blank=False, null=False, default=" ")
    card_type = models.CharField(max_length=50, blank=False, null=False, default=" ")
    card_text = models.CharField(max_length=200, blank=False, null=False, default=" ")
    inventory = models.ForeignKey(Inventory, null=True, on_delete=models.CASCADE)

    def __str__(self):
        try:
            return "Card=[card_name={},card_status={},card_rarity={},card_set={},card_cost={},card_color={},card_type={},card_text={},inventory={}]".format(
                self.card_name,
                self.card_status,
                self.card_rarity,
                self.card_set,
                self.card_cost,
                self.card_color,
                self.card_type,
                self.card_text,
                self.inventory,
            )
        except:
            return "Card=[card_name={},card_status={},card_rarity={},card_set={},card_cost={},card_color={},card_type={},card_text={},inventory={}]".format(
                self.card_name,
                self.card_status,
                self.card_rarity,
                self.card_set,
                self.card_cost,
                self.card_color,
                self.card_type,
                self.card_text,
                self.inventory_id,
            )


class Loaned_Inventory(models.Model):
    loaned_inventory_name = models.CharField(max_length=50, blank=False, null=False, default=" ")
    loaned_inventory_owner = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    loaned_inventory_view_status = models.CharField(
        max_length=50, blank=False, null=False, default="PUBLIC", choices=(("PUBLIC", "Public"), ("PRIVATE", "Private"))
    )

    class Meta:
        verbose_name_plural = "Loaned Inventories"

    def __str__(self):
        try:
            return "Loaned_Inventory=[loaned_inventory_name={},loaned_inventory_owner={},loaned_inventory_view_status={}]".format(
                self.loaned_inventory_name, self.loaned_inventory_owner, self.loaned_inventory_view_status
            )
        except:
            return "Loaned_Inventory=[loaned_inventory_name={},loaned_inventory_owner={},loaned_inventory_view_status={}]".format(
                self.loaned_inventory_name, self.loaned_inventory_owner_id, self.loaned_inventory_view_status
            )


class Loan_Request(models.Model):
    requestor = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    loaner_inventory = models.ForeignKey(Inventory, null=True, on_delete=models.CASCADE)
    loanee_inventory = models.ForeignKey(Loaned_Inventory, null=True, on_delete=models.CASCADE)
    loan_request_status = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        default="REQUESTED",
        choices=(("REQUESTED", "Requested"), ("ACCEPTED", "Accepted"), ("DECLINED", "Declined")),
    )


    class Meta:
        verbose_name_plural = "Loan Requests"

    def __str__(self):
        try:
            return "Loan_Request=[requestor={},loaner_inventory={},loanee_inventory={},loan_request_status={}]".format(
                self.requestor, self.loaner_inventory, self.loanee_inventory, self.loan_request_status
            )
        except:
            return "Loan_Request=[requestor={},loaner_inventory={},loanee_inventory={},loan_request_status={}]".format(
                self.requestor_id, self.loaner_inventory_id, self.loanee_inventory_id, self.loan_request_status
            )


class Loaned_Card(models.Model):
    card = models.ForeignKey(Card, null=True, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, null=True, on_delete=models.CASCADE)
    loan_request = models.ForeignKey(Loan_Request, null=True, on_delete=models.CASCADE)
    loaned_inventory = models.ForeignKey(Loaned_Inventory, null=True, on_delete=models.CASCADE)
    returned_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Loaned Cards"

    def __str__(self):
        try:
            return "Loaned_Card=[card={},inventory={},loan_request={},loaned_inventory={},returned_date={}]".format(
                self.card, self.inventory, self.loan_request, self.loaned_inventory, self.returned_date
            )
        except:
            return "Loaned_Card=[card={},inventory={},loan_request={},loaned_inventory={},returned_date={}]".format(
                self.card_id, self.inventory_id, self.loan_request_id, self.loaned_inventory_id, self.returned_date
            )


@receiver(post_save, sender=Magic_User)
def create_required_tables(sender, instance, created, **kwargs):
    if created:
        Inventory.create(instance.username + "'s inventory", instance).save()
