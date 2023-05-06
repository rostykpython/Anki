# AnkiPetProject

AnkiPetProject is a Python-based application that allows you to convert raw information in plain text into Anki flashcards using the OpenAI API. The application is designed with a user-friendly interface, making it easy to create and manage your flashcards.

![Main screen](https://user-images.githubusercontent.com/89851597/236620554-1e01ca53-b56b-428b-a9b5-ae546aefc0fb.png)

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Convert raw information into Anki flashcards
- User-friendly interface for managing flashcards
- OpenAI API integration for flashcard creation
- Customizeable flashcard appearance

## Requirements
- Python 3.10 or later
- Poetry for package management

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ankipetproject.git
   ```
2. Change to the project directory:
   ```
   cd ankipetproject
   ```
3. Install the required dependencies using Poetry:
   ```
   poetry install
   ```
4. Create a `config.json` file in the project root directory with your OpenAI API key and desired model:
   ```
   {
       "API_KEY": "your_openai_api_key",
       "MODEL": "your_model_name"
   }
   ```

## Usage
1. To run the AnkiPetProject application, use the following command:
   ```
   poetry run python main.py
   ```
2. The application will open, and you can start by managing your API key or creating flashcards.

### Manage API Key
![image](https://user-images.githubusercontent.com/89851597/236620537-6e53a7b9-5b08-43a7-a17d-a11ec5bee3ae.png)
1. Click on the "Manage API key" button to open the API key management scene.
2. Add or update your OpenAI API key and model, then click "Save" to store the information in the `config.json` file.

### Create Flashcards
![image](https://user-images.githubusercontent.com/89851597/236620643-5c4a1c0c-5241-4184-a8aa-f8d6aa24a888.png)
1. Click on the "Create flashcards" button to open the flashcard creation scene.
2. Enter your raw information in the text box and click "Create Flashcards" to generate Anki flashcards using the OpenAI API.
3. The created flashcards will be displayed, and you can edit or delete them as needed.
![image](https://user-images.githubusercontent.com/89851597/236620722-728ae0fd-8a8f-49d5-8750-6b9b03cbc706.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)
Please ensure you follow the [Code of Conduct](CODE_OF_CONDUCT.md) when contributing to this project.

## Support
If you encounter any issues or have questions, please open an issue on the GitHub repository.

## Acknowledgements
- [OpenAI](https://www.openai.com/) for providing the GPT model and API
- [genanki](https://github.com/kerrickstaley/genanki) for Anki flashcard generation
- [customtkinter](https://github.com/jrenner/customtkinter) for creating custom-themed Tkinter widgets
- [Poetry](https://python-poetry.org/) for Python dependency management

We hope that AnkiPetProject will help you create Anki flashcards more efficiently and enhance your learning experience. Enjoy using the application!
