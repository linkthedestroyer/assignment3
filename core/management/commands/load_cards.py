import json
import os
import random
from os import listdir
from os.path import isfile, join

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from models.models import (
    CARD_CHOICES,
    Card,
    Inventory,
    Loan_Request,
    Loaned_Card,
    Loaned_Inventory,
)

# Place JSON and CSV file in import_data folder
FOLDER_PATH = os.path.join(settings.BASE_DIR, "scry_fall_data")


def get_oracle_text(card_faces):
    return card_faces["oracle_text"]


# NOTE Extends base command which is how django recongizes the script
# If you want to create your own command you MUST put it in a sub app folder structure
# Under the management/command folders
class Command(BaseCommand):
    help = "Gets a random set of cards and adds it to the database"

    def handle(self, *args, **options):
        # This calls the flush django command to strip out all database data
        Card.objects.all().delete()
        Loaned_Card.objects.all().delete()
        Loaned_Inventory.objects.all().delete
        # gets array of all file names in the import_data folder
        with open(
            os.path.join(FOLDER_PATH, "CARD_DATA_LIST.json"),
            encoding="utf8",
            newline="",
        ) as file_object:
            card_data = json.load(file_object)
            already_inserted = []
            for x in range(0, 1000):
                random_index = random.randint(0, len(card_data["data_list"]) - 1)
                random_card = card_data["data_list"][random_index]
                while (
                    random_index in already_inserted
                    or random_card["set_type"] == "memorabilia"
                    or random_card["layout"] == "token"
                ):
                    random_index = random.randint(0, len(card_data["data_list"]) - 1)
                    random_card = card_data["data_list"][random_index]

                already_inserted.append(random_index)
                try:
                    new_card = Card()
                    new_card.card_name = random_card["name"]
                    new_card.card_status = CARD_CHOICES[random.randint(0, 3)][0]
                    new_card.card_rarity = random_card["rarity"]
                    new_card.card_set = random_card["set_name"]
                    new_card.card_cost = random_card["mana_cost"]
                    new_card.card_color = "".join(random_card["colors"])
                    new_card.card_type = random_card["type_line"]
                    try:
                        new_card.card_text = random_card["oracle_text"]
                    except:
                        new_card.card_text = " ".join(map(get_oracle_text, random_card["card_faces"]))
                    new_card.card_img_url = random_card["image_uris"]["normal"]
                    new_card.inventory = random.choice(list(Inventory.objects.all()))
                    new_card.save()
                except Exception as error:
                    print("Could not save the random card")
                    print(random_card)
                    print(error)
                    x -= 1
            print(len(Card.objects.all()))
            cards_to_loan: Card = Card.objects.filter(card_status="LOANED_OUT")
            for card_to_loan in cards_to_loan:
                try:
                    loaned_inventory: Loaned_Inventory = random.choice(list(Loaned_Inventory.objects.all()))
                    new_loan_request = Loan_Request()
                    new_loan_request.requestor = loaned_inventory.loaned_inventory_owner
                    new_loan_request.loaner_inventory = card_to_loan.inventory
                    new_loan_request.loanee_inventory = loaned_inventory
                    new_loan_request.loan_request_status = [
                        "REQUESTED",
                        "ACCEPTED",
                        "DECLINED",
                        "RECALLED",
                        "RETURNED",
                    ][random.randint(0, 4)]
                    new_loan_request.save()
                    new_loaned_card = Loaned_Card()
                    new_loaned_card.card = card_to_loan
                    new_loaned_card.loan_request = new_loan_request
                    new_loaned_card.save()
                except Exception as error:
                    print("Could not save loaned card")
                    print(cards_to_loan)
                    print(error)
            print(len(Loaned_Card.objects.all()))
