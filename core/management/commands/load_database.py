import json
import os
import random
from os import listdir
from os.path import isfile, join

from models.models import Card, Inventory, Loan_Request, Loaned_Card, Loaned_Inventory
from users.models import Magic_User
from django.apps.config import AppConfig
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand

# Place JSON and CSV file in import_data folder
FOLDER_PATH = os.path.join(settings.BASE_DIR, 'import_data')

# NOTE Extends base command which is how django recongizes the script
# If you want to create your own command you MUST put it in a sub app folder structure
# Under the management/command folders
class Command(BaseCommand):
    help = 'Sets data for all models'

    def handle(self, *args, **options):
        # This calls the flush django command to strip out all database data
        call_command('flush', verbosity=0, interactive=False)
        # gets array of all file names in the import_data folder
        import_files = [f for f in listdir(FOLDER_PATH) if isfile(join(FOLDER_PATH, f))]
        try_again_files = []
        for file in import_files:
            # gets the model name from file name
            model_class_name = file.split(".")[0]
            if model_class_name == 'Loaned_Card':
                continue
            try:
                # Tries to find the named model
                model_class = eval(model_class_name)
            except:
                # if it can't find it goes to the next file
                print("Could not find: " + model_class_name + ". Please try to fix the file: " + file)
                continue
            # Opens the file

            with open(os.path.join(FOLDER_PATH, file), newline='') as file_object:
                # If csv file
                if file.split(".")[1].lower() == 'json':
                    # JSON Path
                    data = json.load(file_object)
                    if model_class_name == 'Magic_User' or model_class_name == 'User':
                        for raw_example_data in data['data_array']:
                            user: Magic_User = Magic_User.objects.create_user(
                                first_name=raw_example_data['first_name'],
                                last_name=raw_example_data['last_name'],
                                username=raw_example_data['username'],
                                password=raw_example_data['password'],
                                email=raw_example_data['email'],
                                is_staff=raw_example_data['is_staff'],
                                is_superuser=(
                                    raw_example_data['is_superuser'] if 'is_superuser' in raw_example_data else False
                                ),
                                is_active=raw_example_data['is_active'],
                                date_joined=raw_example_data['date_joined'] + 'T00:00:00-05:00',
                                last_login=raw_example_data['last_login'] + '-05:00',
                                phone_number=raw_example_data['phone_number'],
                                address=raw_example_data['address'],
                            )
                            try:
                                user.save()
                            except:
                                print('Tried to save ' + user.__str__())
                    else:
                        tryAgain = handleJSON(data, model_class)
                        if tryAgain:
                            try_again_files.append(model_class_name + '.json')

            # print out the models saved
            for new_model in model_class.objects.all():
                print(new_model.__str__())
            # print out the number of objects in the model
            print(model_class.objects.all().__len__())

        try_count = try_again_files.__len__() * 3
        index = 0
        while try_again_files.__len__() > 0 and index < try_count:
            index += 1
            try_again: str = try_again_files.pop()
            print('Trying again with file: ' + try_again + ', try index count: ' + str(index))
            model_class_name = try_again[try_again.rfind('\\') + 1 :].split(".")[0]
            try:
                # Tries to find the named model
                model_class = eval(model_class_name)
            except:
                # if it can't find it goes to the next file
                print("Could not find: " + model_class_name + ". Please try to fix the file: " + file)
                continue
            with open(os.path.join(FOLDER_PATH, try_again), newline='') as file_object:
                data = json.load(file_object)
                tryAgain = handleJSON(data, model_class)
                if tryAgain:
                    try_again_files.insert(0, try_again)
                    continue

            for new_model in model_class.objects.all():
                print(new_model.__str__())
            # print out the number of objects in the model
            print(model_class.objects.all().__len__())

        with open(os.path.join(FOLDER_PATH, 'Loaned_Card.json'), newline='') as file_object:
            data = json.load(file_object)
            for raw_example_data in data['data_array']:
                card_id = raw_example_data['card_id']
                card = Card.objects.get(pk=card_id)
                loan_request: Loan_Request = random.choice(list(Loan_Request.objects.all()))
                inventory = loan_request.loaner_inventory
                loaned_inventory = loan_request.loanee_inventory
                loaned_card = Loaned_Card()
                loaned_card.card = card
                loaned_card.inventory = inventory
                loaned_card.loan_request = loan_request
                loaned_card.loaned_inventory = loaned_inventory
                loaned_card.save()


def handleJSON(data, model_class) -> bool:
    for raw_example_data in data['data_array']:
        # New model again
        new_model = model_class()
        for ignored, key in enumerate(raw_example_data.keys()):
            # grabs the key data and sets it
            data = raw_example_data[key]
            if key.find('dateTime') >= 0:
                data = data + '-05:00'
            setattr(new_model, key, data)
        try:
            # saves it
            new_model.save()
        except Exception as e:
            print(e)
            print('There was a problem ' + new_model.__str__())
            return True
    return False
