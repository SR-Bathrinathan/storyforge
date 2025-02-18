# StoryForge

StoryForge is an AI-powered storytelling appliclication that generates unique short stories based on user-defined parameters. It utilizes OpenAI's GPT-4o for text generation and Hugging Face's models for image and audio generation. This allows for multi-modal consumption which allows our brain to have a deeper understanding by interpreting the data in multiple formats.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Generate AI-powered short stories
- Extract key events from stories
- Generate images based on story context
- Convert stories to audio

## Installation

### Prerequisites
- Python 3.8+
- pip
- An OpenAI API key (for text generation)
- A Hugging Face API key (for image and audio generation)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/StoryForge.git
   cd StoryForge
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
    Open `.env` and add your API keys:
     ```sh
     OPENAI_API_KEY=your_openai_api_key_here
     HUGGINGFACE_API_KEY=your_huggingface_api_key_here
     ```

## Usage

### Running the Application
Start the Streamlit web app:
```sh
streamlit run src/app.py
```

### How It Works
1. Select the **genre**, **tone**, **mood**, and **point of view** for your story.
2. Select the number of charecters and add their details. 
3. Click **"Generate Story"** to create a unique short story, whose audio and key-event images are generated
4. The generated contents are finally displayed.

## Contributing
Pull requests are welcome! If you'd like to improve StoryForge, please fork the repository and submit a PR.

## License
This project is licensed under The Unlicense License.
For more information, please refer to <http://unlicense.org/>
