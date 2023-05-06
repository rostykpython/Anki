import json
import requests
from typing import Union, Dict


def invoke(action: str, **params: Union[str, int]) -> Dict[str, Union[None, str]]:
    """
    Invoke AnkiConnect API with given action and parameters.

    :param action: The name of the AnkiConnect action to be executed.
    :param params: Keyword arguments for the action's parameters.
    :return: A dictionary containing the result of the action.
    """

    try:
        request_json = json.dumps({'action': action, 'params': params, 'version': 6})
        response = requests.post('http://localhost:8765', data=request_json)
        return response.json()
    except ConnectionError as error:
        return {"error": str(error)}


def save_package_to_app(package_path: str) -> None:
    """
    Save the Anki package to the application using AnkiConnect.

    :param package_path: The path of the Anki package to be imported.
    """

    result = invoke('importPackage', path=package_path)

    if result['error'] is None:
        print('Deck imported successfully')
    else:
        print('Error importing deck:', result['error'])

