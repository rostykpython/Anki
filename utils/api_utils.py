import os
import json


def load_api_data():
    """
    Load API data from the config.json file if it exists.

    :return: A dictionary containing the API data, or an empty dictionary if the file does not exist.
    """

    if os.path.exists(os.path.join(os.getcwd(), "config.json")):
        with open("config.json", "r") as js_api:
            return json.load(js_api)
    return {}
