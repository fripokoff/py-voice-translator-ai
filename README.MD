# Voice Translator

Voice Translator is a Python project that transcribes, translates, and converts `.wav` audio files into spoken text. It uses several libraries, including `speech_recognition` for transcription, `googletrans` for translation, and `gtts` for text-to-speech conversion.

## Prerequisites

To run this project, you will need Python 3.6 or higher. You will also need several Python libraries, which are listed in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```
Additionally, this project uses `pydub` to handle audio files, which requires `ffmpeg`. Therefore, you need to download `ffmpeg` and place it in the root of your project.
[FFMPEG](https://ffmpeg.org/download.html)

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Install the necessary dependencies.
4. Download ffmpeg.
5. Unzip the downloaded file and place the ffmpeg folder in the root of your project.

## Usage
To use this project, place a .wav file in the project directory, then run the voice_translator.py script with the following command:python voice_translator.py

The script will prompt you to choose the source language of the audio and the language you want to translate the text into. It will then transcribe the audio, translate the text, and convert the translated text into spoken audio. The translated audio will be saved in a .mp3 file.

During the language selection process, you can enter '0' to go back to the previous step.