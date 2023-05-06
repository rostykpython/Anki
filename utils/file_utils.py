import os
import customtkinter as ctk
from PIL import Image
from typing import Tuple


def get_package_dir():
    """
    Get the deck packages directory path.

    :return: The deck packages directory path as a string.
    """
    return os.path.join(os.getcwd(), "deck_packages")


def get_icons_dir():
    """
    Get the icons directory path.

    :return: The icons directory path as a string.
    """
    return os.path.join(os.getcwd(), "icons")


def get_icon(icon_name: str, size: Tuple = (30, 30)):
    """
    Get a custom tkinter image object for the specified icon.

    :param icon_name: The name of the icon file.
    :param size: A tuple containing the width and height of the icon (default: (30, 30)).
    :return: A custom tkinter image object.
    """

    icons_dir = get_icons_dir()
    icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, icon_name)), size=size)
    return icon
