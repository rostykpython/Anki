import os

import tkinter as tk
import customtkinter as ctk
import openai

from ui_components import Scene1, Scene2
from utils.api_utils import load_api_data
from utils.file_utils import get_icon

OPENAI_APIKEY = ""
GPT_MODEL = ""

if os.path.exists(os.path.join(os.getcwd(), "config.json")):
    api_data = load_api_data()
    OPENAI_APIKEY = api_data["API_KEY"]
    GPT_MODEL = api_data["MODEL"]

openai.api_key = OPENAI_APIKEY

# System settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """Main class for the Anki cards creator application."""

    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Anki cards creator")

        self.api_keys_scene = None
        self.scenes_params = dict(row=0, column=1, sticky=tk.NSEW)

        self.left_frame = ctk.CTkFrame(self, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="NS")

        self.manage_api = ctk.CTkButton(self.left_frame,
                                        text="Manage API key",
                                        command=self.change_to_api_scene,
                                        width=150,
                                        height=35,
                                        fg_color="gray20",
                                        hover_color="gray25",
                                        image=get_icon("key.png", (18, 18)))

        self.manage_api.pack(padx=10, pady=10)

        self.createing_flashcards = ctk.CTkButton(self.left_frame,
                                                  text="Create flashcards",
                                                  width=150,
                                                  height=35,
                                                  fg_color="gray20",
                                                  hover_color="gray25",
                                                  image=get_icon("plus.png", (20, 20)),
                                                  command=self.change_to_flashcard_scene)

        self.createing_flashcards.pack(padx=10, pady=10)

        self.quit_btn = ctk.CTkButton(self.left_frame,
                                      text="Quit",
                                      width=150,
                                      fg_color="gray20",
                                      hover_color="gray25",
                                      image=get_icon("leave.png", (15, 15)),
                                      command=self.quit)
        self.quit_btn.pack(pady=10, side=tk.BOTTOM)

        self.flash_card_scene = Scene1(self, fg_color="#f7f7f8", corner_radius=0)
        self.flash_card_scene.grid(**self.scenes_params)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def change_to_api_scene(self):
        """Switch the displayed scene to the API key management scene."""

        self.flash_card_scene.forget()
        self.api_keys_scene = Scene2(self, fg_color="#f7f7f8", corner_radius=0)
        self.api_keys_scene.grid(**self.scenes_params)

    def change_to_flashcard_scene(self):
        """Switch the displayed scene to the flashcard creation scene."""

        self.api_keys_scene.forget()
        self.flash_card_scene = Scene1(self, fg_color="#f7f7f8", corner_radius=0)
        self.flash_card_scene.grid(**self.scenes_params)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
