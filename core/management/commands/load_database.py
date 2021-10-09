import csv
import json
import os
from os import listdir
from os.path import isfile, join

from django.apps.config import AppConfig
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict
from models.models import *
from users.models import *

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
        for file in import_files:
            # gets the model name from file name
            model_class_name = file.split(".")[0]
            try:
                # Tries to find the named model
                model_class = eval(model_class_name)
            except:
                # if it can't find it goes to the next file
                print("Could not find: " + model_class_name + ". Please try to fix the file: " + file)
                continue
            # Gets all the keys of the model (including 'id')
            objectKeys = model_to_dict(model_class()).keys()
            # Opens the file
            with open(os.path.join(FOLDER_PATH, file), newline='') as file_object:
                # If csv file
                if file.split(".")[1].lower() == 'csv':
                    # Use default python code to read each line
                    reader = csv.reader(file_object, delimiter=',', quotechar='|')
                    for row in reader:
                        # create new model
                        new_model = model_class()
                        for index, key in enumerate(objectKeys):
                            # skips index 0 because that is 'id' and we shouldn't set that
                            if index != 0:
                                # Uses setattr to set the model key value
                                setattr(new_model, key, row[index - 1])
                        try:
                            # Saves the data
                            new_model.save()
                        except:
                            print("there was a problem with line: " + new_model.__str__())
                else:
                    # JSON Path
                    data = json.load(file_object)
                    for raw_example_data in data['data_array']:
                        # New model again
                        new_model = model_class()
                        for index, key in enumerate(raw_example_data):
                            # grabs the key data and sets it
                            setattr(new_model, key, raw_example_data[key])
                        try:
                            # saves it
                            new_model.save()
                        except:
                            print("there was a problem with line: " + new_model.__str__())
            # print out the models saved
            for new_model in model_class.objects.all():
                print(new_model.__str__())
            # print out the number of objects in the model
            print(model_class.objects.all().__len__())
