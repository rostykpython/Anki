from typing import Dict


def preprocess_response(text: str) -> Dict[int, Dict[str, str]]:
    """
    Preprocess the given text and create a dictionary of flashcards.

    :param text: Text containing flashcard data.
    :return: A dictionary with integer keys and flashcard data as values.
    """

    try:
        splitted_cards = text.split("\n")
        sorted_cards = list(filter(lambda t: len(t) > 0, splitted_cards))

        cards_dict = {}
        for index, card in enumerate(sorted_cards[::2]):
            question = card.split("Front: ")[-1].strip()
            answer = sorted_cards[index * 2 + 1].split("Back: ")[-1].strip()
            cards_dict[index] = {"question": question, "answer": answer}

        return cards_dict
    except ValueError as err:
        print(f"Error while preprocessing response: {err}")


def create_textbox_text(front: str, back: str) -> str:
    """
    Create a formatted text string for a flashcard's front and back.

    :param front: Text for the front of the flashcard.
    :param back: Text for the back of the flashcard.
    :return: A formatted string containing the front and back of the flashcard.
    """
    ...

    return f"Front: {front}\nBack: {back}"
