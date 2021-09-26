from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from users.models import MagicUser


class Inventory(models.Model):
    inventory_name = models.CharField(max_length=50, blank=False, null=False, default=" ")
    inventory_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    inventory_view_status = models.CharField(
        max_length=50, blank=False, null=False, default="PUBLIC", choices=(("PUBLIC", "Public"), ("PRIVATE", "Private"))
    )

    @classmethod
    def create(cls, inventory_name, user):
        inventory = cls(inventory_name=inventory_name, inventory_owner=user)
        return inventory

    def __str__(self):
        return "{} {}".format(self.inventory_name, self.inventory_owner, self.inventory_view_status)


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
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.card_name, self.inventory)


class Loanee(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @classmethod
    def create(cls, user):
        loanee = cls(user=user)
        return loanee

    def __str__(self):
        return "{}".format(self.user.username)


class Loaner(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @classmethod
    def create(cls, user):
        loaner = cls(user=user)
        return loaner

    def __str__(self):
        return "{}".format(self.user.username)


class Loaned_Inventory(models.Model):
    loaned_inventory_name = models.CharField(max_length=50, blank=False, null=False, default=" ")
    loaned_inventory_view_status = models.CharField(
        max_length=50, blank=False, null=False, default="PUBLIC", choices=(("PUBLIC", "Public"), ("PRIVATE", "Private"))
    )
    loaned_inventory_loanee_user = models.ForeignKey(Loanee, on_delete=models.CASCADE, verbose_name="test")
    loaned_inventory_loaner_user = models.ForeignKey(Loaner, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.loaned_inventory_name, self.loaned_inventory_view_status)


class Loan_Request(models.Model):
    requestor_user = models.ForeignKey(Loanee, on_delete=models.CASCADE)
    loaner_user = models.ForeignKey(Loaner, on_delete=models.CASCADE)
    loan_request_status = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        default="REQUESTED",
        choices=(("REQUESTED", "Requested"), ("ACCEPTED", "Accepted"), ("DECLINED", "Declined")),
    )
    loan_inventory = models.ForeignKey(Loaned_Inventory, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.requestor_user, self.loaner_user, self.loan_request_status)


class Loaned_Card(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    loan_request = models.ForeignKey(Loan_Request, on_delete=models.CASCADE)
    loaned_inventory = models.ForeignKey(Loaned_Inventory, on_delete=models.CASCADE)
    returned_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.card, self.inventory, self.loaned_inventory)

@receiver(post_save, sender=MagicUser)
def create_required_tables(sender, instance, created, **kwargs):
    if created:
        Inventory.create(instance.username + "'s inventory", instance).save()
        Loanee.create(instance).save()
        Loaner.create(instance).save()
