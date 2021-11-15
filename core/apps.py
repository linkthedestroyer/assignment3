import json
import os
import threading
import time
import sys
from pathlib import Path

import requests
from django.apps import AppConfig
from django.conf import settings


def map_code(data: dict):
    new_data = {}
    new_data["code"] = data["code"]
    new_data["name"] = data["name"]
    return new_data


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        if "runserver" in sys.argv:
            get_data_thread = threading.Thread(target=thread_function, args=(1,))
            print("Config    : before running thread")
            get_data_thread.start()
            print("Config    : all done")


def thread_function(name):
    # prevents multiple reloads from overloading scryfall and getting my local pc banned
    print("Thread {}: starting".format(name))
    time.sleep(90)
    path = Path(os.path.join(settings.STATIC_ROOT, "sets/sets.json"))
    path.touch(exist_ok=True)
    with open(path, "w") as file:
        response = requests.get("https://api.scryfall.com/sets")
        data_array = response.json()["data"]
        code_array = list(map(map_code, data_array))
        outfile = {}
        outfile["data"] = code_array
        json.dump(outfile, file)
    print("Thread {}: finishing".format(name))
