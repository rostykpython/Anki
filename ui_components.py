import os
import threading
import random
import json

import tkinter as tk
import customtkinter as ctk

import openai
from genanki import Model, Note, Deck, Package

from utils.text_preprocessing_utils import preprocess_response, create_textbox_text
from utils.anki_connection_utils import save_package_to_app
from utils.api_utils import load_api_data
from utils.file_utils import get_package_dir, get_icon


class CustomCTkTextbox(ctk.CTkTextbox):
    """Custom text box with added functionality for state management."""

    def __init__(self, master=None, **kwargs):
        """Initialize the custom text box."""

        super().__init__(master, **kwargs)
        self.custom_state = "normal"

    def set_state(self, state):
        """Set the custom state of the text box."""

        self.custom_state = state

        italic_font = ctk.CTkFont(family="Helvetica", size=12, slant="italic")

        if state == "disabled":
            self.configure(text_color="gray",
                           font=italic_font,
                           state=state)
        else:
            self.configure(text_color="black")

    def get_state(self):
        """Get the current custom state of the text box."""

        return self.custom_state


class PopUpWindow(ctk.CTkToplevel):
    """Pop-up window to show successful save messages."""

    def __init__(self, *args, **kwargs):
        """Initialize the pop-up window."""

        super().__init__(*args, **kwargs)

        x = int(self.winfo_screenwidth() // 2)
        y = int(self.winfo_screenheight() // 2)

        self.geometry(f"200x150+{x}+{y}")
        self.process_state_label = ctk.CTkLabel(self, text="Successfully saved!", text_color="green")
        self.process_state_label.pack(padx=10, pady=10)

        self.save_btn = ctk.CTkButton(self,
                                      width=60,
                                      height=40,
                                      text="Ok",
                                      command=self.destroy)

        self.save_btn.pack(padx=10, pady=10)


class ToplevelWindow(ctk.CTkToplevel):
    """Top-level window to display and manage flashcards."""

    PACKAGE_DIR = get_package_dir()

    SAVE_ICON = get_icon("save.png")
    DELETE_ICON = get_icon("delete.png")
    SUCCESS_ICON = get_icon("success.png")
    FAIL_ICON = get_icon("fail.png")

    def __init__(self, flash_cards, *args, **kwargs):
        """Initialize the top-level window."""

        super().__init__(*args, **kwargs)
        self.MODEL_ID = self.generate_random_id()

        self.model = Model(
            self.MODEL_ID,
            'Flash card model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ])

        self.notes = []
        self.DECK_ID = self.generate_random_id()
        self.deck = Deck(self.DECK_ID, '')

        self.flash_cards = flash_cards

        self.geometry("800x640")

        self.ctframes = []

        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color=self.cget("fg_color"))
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.deck_title = ctk.CTkEntry(self.scrollable_frame, width=300,
                                       placeholder_text="Entry deck title...",
                                       placeholder_text_color="grey")

        self.deck_title.pack(padx=10, pady=10)

        for card_id in range(len(flash_cards)):
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.scrollable_frame.cget("fg_color"))
            row_frame.pack(padx=10, pady=5)

            tbox = CustomCTkTextbox(row_frame, width=600, height=150,
                                    border_spacing=8, wrap="word")

            tbox.pack(side=tk.LEFT, expand=True, fill=tk.X)
            tbox.insert(0.0, create_textbox_text(
                flash_cards[card_id]["question"],
                flash_cards[card_id]["answer"]
            ))

            delete_btn = ctk.CTkButton(row_frame,
                                       text="",
                                       image=self.DELETE_ICON,
                                       width=8,
                                       command=lambda i=card_id: self.process_card(flash_cards[i],
                                                                                   self.ctframes[i],
                                                                                   method="delete"))

            delete_btn.pack(padx=10, pady=10, side=tk.RIGHT)

            save_btn = ctk.CTkButton(row_frame,
                                     text="",
                                     image=self.SAVE_ICON,
                                     width=8,
                                     command=lambda i=card_id: self.process_card(flash_cards[i],
                                                                                 self.ctframes[i],
                                                                                 method="save"))

            save_btn.pack(padx=10, pady=10, side=tk.RIGHT)

            self.ctframes.append(row_frame)

        self.button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=self.cget("fg_color"))
        self.button_frame.pack(padx=10, pady=10)

        self.save_to_anki_btn = ctk.CTkButton(self.button_frame,
                                              text="Save to Anki",
                                              state="disabled",
                                              command=lambda: self.save_to_anki(self.deck_title.get()))

        self.save_to_anki_btn.pack(padx=10, pady=10, side=tk.LEFT)

        self.back_to_main = ctk.CTkButton(self.button_frame,
                                          text="Back",
                                          command=self.get_to_mainwindow)

        self.back_to_main.pack(padx=10, pady=10, side=tk.RIGHT)

    def set_label_image(self, label, success):
        """Set the appropriate image for the label depending on the success status."""

        label.configure(image=self.SUCCESS_ICON if success else self.FAIL_ICON)

    def disable_widgets(self, frame, method: str = "save"):
        """Disable the widgets and remove buttons in the frame after processing."""

        for child in frame.winfo_children():
            if isinstance(child, CustomCTkTextbox):
                child.set_state("disabled")

            if isinstance(child, ctk.CTkButton):
                child.destroy()

        process_label = ctk.CTkLabel(frame, text="")
        self.set_label_image(process_label, method == "save")
        process_label.pack(padx=10, pady=10, side=tk.RIGHT)

    def process_card(self, flash_card, current_frame, method="save"):
        """Process the flashcard based on the selected method (save or delete)."""

        if method == "save":
            note = Note(
                model=self.model,
                fields=[flash_card["question"], flash_card["answer"]],
            )

            self.notes.append(note)

        self.disable_widgets(current_frame, method)

        all_disabled = True

        for child in self.scrollable_frame.winfo_children():
            if isinstance(child, ctk.CTkFrame) and any(
                    [frame_child.custom_state != "disabled" for frame_child in child.winfo_children() if
                     isinstance(frame_child, CustomCTkTextbox)]):
                all_disabled = False

        if all_disabled:
            self.save_to_anki_btn.configure(state="normal")

    def save_to_anki(self, deck_title):
        """Save the generated flashcards to an Anki deck."""

        for note in self.notes:
            self.deck.add_note(note)

        if len(deck_title) <= 0:
            deck_title = f"Package{self.generate_random_id()}"

        filename = f"{deck_title}.apkg"
        self.deck.name = deck_title
        Package(self.deck).write_to_file(os.path.join(self.PACKAGE_DIR, filename))

        self.save_to_anki_btn.configure(state="disabled")

        save_package_to_app(os.path.join(self.PACKAGE_DIR, filename))

        popup = PopUpWindow(self)
        popup.focus_force()

    def get_to_mainwindow(self):
        """Return to the main window."""

        self.master.focus()
        self.destroy()

    @staticmethod
    def generate_random_id():
        """Generate a random ID for decks and models."""

        return random.randint(10 ** 9, 10 ** 10 - 1)


class Scene1(ctk.CTkFrame):
    """Flashcard creation scene for the Anki cards creator application."""

    content_msg = "You are an AI-powered assistant that creates AnkiWeb flashcards from the text. " \
                  "Your task is to identify the most significant and relevant information from the " \
                  "text and generate flashcards with the following format:" \
                  "Front: [question to test knowledge retention]" \
                  "Back: [answer to the question]" \
                  "\nImportant requirement: If text is not appropriate, you should reply with " \
                  "'Unable to generate flashcards'. Only with this sentence and nothing else"

    def __init__(self, *args, **kwargs):
        """
        Initialize the flashcard creation scene.

        :param master: Parent widget for the Scene1 class.
        :param kw: Additional keyword arguments for the scene configuration.
        """

        super().__init__(*args, **kwargs)
        # Adding UI Elements
        title = ctk.CTkLabel(self, text="Insert your text", text_color="black")
        title.grid(row=0, column=1, padx=10, pady=10, sticky="NS")

        # Button frame
        self.main_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))

        # Text input
        self.text = ctk.CTkTextbox(self, width=650, height=400, corner_radius=8,
                                   activate_scrollbars=True, border_spacing=6, wrap="word")

        self.text.grid(row=1, column=1, padx=10, pady=10, sticky=tk.NSEW)

        # Preprocessing text
        create_flashcards = ctk.CTkButton(self.main_frame,
                                          text="Create flashcards",
                                          command=self.start_creation,
                                          )
        create_flashcards.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # Clear textbox

        clear_textbox = ctk.CTkButton(self.main_frame, text="Clear", command=lambda: self.text.delete(1.0, tk.END))
        clear_textbox.grid(row=0, column=1, padx=10, pady=10)

        self.main_frame.grid(row=2, column=1, padx=10, pady=10, sticky="NS")

        # Progressbar
        self.progress_bar = ctk.CTkProgressBar(self,
                                               width=400,
                                               mode="indeterminate",
                                               indeterminate_speed=0.9)

        self.progress_bar._indeterminate_width = 0.3
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=1, padx=10, pady=10, sticky="NS")

        self.toplevel_window = None

        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def open_toplevel(self, flash_cards):
        """Open a new top-level window to display flashcards."""

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(flash_cards)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def chat_completion(self, text_info):
        """Submit user input to the GPT model and get the generated flashcards."""

        try:
            gpt_response = openai.ChatCompletion.create(
                model=load_api_data().get("MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system",
                     "content": self.content_msg},
                    {"role": "user",
                     "content": text_info}
                ]
            )

            flash_cards_text = gpt_response.get("choices")[0]["message"]["content"]
            return flash_cards_text
        except Exception as error:
            print(error)
            return "Some error ackward!\nTry to add or change API key"

    def start_chat_completion(self):
        """Start the chat completion process and update the progress bar."""

        user_input = self.text.get("1.0", ctk.END)
        self.progress_bar.start()
        response_thread = threading.Thread(target=self.run_chat_completion, args=(user_input,))
        response_thread.start()

        while response_thread.is_alive():
            self.progress_bar.update()

        self.progress_bar.stop()

    def run_chat_completion(self, user_input):
        """Run the chat completion process and display the results."""

        response = self.chat_completion(user_input)
        self.progress_bar.stop()

        if response.startswith("Some error"):
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, response)
        else:
            flash_cards_dict = preprocess_response(response)
            self.open_toplevel(flash_cards_dict)

    def start_creation(self):
        """Initiate the process of creating flashcards."""

        try:
            self.start_chat_completion()
        except Exception as e:
            print(f"An error occurred: {e}")


class Scene2(ctk.CTkFrame):
    """API key management scene for the Anki cards creator application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """
        Initialize the API key management scene.

        :param master: Parent widget for the Scene2 class.
        :param kw: Additional keyword arguments for the scene configuration.
        """

        self.text_label = ctk.CTkLabel(self, text="Insert you API key", text_color="black")
        self.text_label.grid(row=0, column=1, padx=10, pady=20, sticky=tk.NSEW)

        self.api_data = load_api_data()

        self.entry_api = ctk.CTkEntry(self, placeholder_text="Add API-key here...", width=600)
        self.entry_api.grid(row=1, column=1, padx=10, pady=20)
        self.entry_api.insert(tk.END, self.api_data.get("API_KEY", ""))

        self.combo_model = ctk.CTkComboBox(self,
                                           values=["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-4", "gpt-4-0314"],
                                           state="readonly",
                                           width=200
                                           )
        self.combo_model.grid(row=2, column=1, padx=10, pady=20)
        self.combo_model.set(self.api_data.get("MODEL", "gpt-3.5-turbo"))

        self.save_apikey = ctk.CTkButton(self, width=150, text="Save API-key", command=self.save_api_key)
        self.save_apikey.grid(row=3, column=1, padx=10, pady=20, )

        self.columnconfigure(1, weight=1)

    def save_api_key(self):
        """Save the API key to the specified file."""

        api_key = self.entry_api.get()

        with open("config.json", "w") as js_file:
            json.dump(
                {"API_KEY": api_key,
                 "MODEL": str(self.combo_model.get())},
                js_file)

        openai.api_key = api_key
        self.save_apikey.configure(state="disable", fg_color="grey", command=None)

        label_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        label_frame.grid(row=4, column=1, padx=10, )

        success_image_label = ctk.CTkLabel(label_frame,
                                           text="",
                                           image=get_icon("success.png", (15, 15)))
        success_image_label.grid(row=0, column=0, padx=5, pady=5)

        success_text_label = ctk.CTkLabel(label_frame,
                                          text="Saved",
                                          text_color="green")
        success_text_label.grid(row=0, column=1, padx=5, pady=10)




