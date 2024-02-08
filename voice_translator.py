import os
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import threading
import time
import sys
from googletrans import LANGUAGES
from fuzzywuzzy import process
import random

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def get_wav():
	files = os.listdir()
	wav_files = [file for file in files if file.endswith('.wav')]
	if not wav_files:
		print("No .wav files found in the current directory.")
		sys.exit(1)
	return wav_files[0]

wav = get_wav()

def set_engine(engine):
	clear_screen()
	sys.stdout.write(f"Audio: {wav.capitalize()}\nEngine: {engine.capitalize()}")
	sys.stdout.flush()
	return engine

engine_choice = set_engine('Google')
language = None
audio_language = None

def split_audio(audio_file, segment_duration_ms):
	audio = AudioSegment.from_wav(audio_file)
	segments = []
	for i in range(0, len(audio), segment_duration_ms):
		segments.append(audio[i:i+segment_duration_ms])
	return segments

def transcribe_audio_to_text(audio_file, language_code):
	r = sr.Recognizer()
	segments = split_audio(audio_file, segment_duration_ms=60000)
	text = ""
	def display_percentage():
		nonlocal transcribing
		start_time = time.time()
		slow_progress_limit = random.uniform(90, 95)
		while transcribing:
			elapsed_time = time.time() - start_time
			if elapsed_time < 30:
				percentage = min((elapsed_time / 30) * 100, slow_progress_limit)
			else:
				percentage = slow_progress_limit + min((elapsed_time - 30) / 30, 20)
			sys.stdout.write(f"\rTranscribing segment {i+1} of {len(segments)}... [{percentage:.2f}%]")
			sys.stdout.flush()
			time.sleep(0.1)

	for i, segment in enumerate(segments):
		transcribing = True
		progress_thread = threading.Thread(target=display_percentage)
		progress_thread.start()
		segment.export('temp.wav', format='wav')

		with sr.AudioFile('temp.wav') as source:
			audio_data = r.record(source)
			text += r.recognize_google(audio_data, language=language_code)

		sys.stdout.write(f"\rProgress: 100.00%")
		transcribing = False
		progress_thread.join()
		os.remove('temp.wav')

	return text

def split_text(text, segment_length):
	words = text.split()
	segments = []
	for i in range(0, len(words), segment_length):
		segments.append(' '.join(words[i:i+segment_length]))
	return segments

def translate_text(text, dest_language):
	translator = Translator()
	segments = split_text(text, segment_length=5000)
	translated_text = ""

	for i, segment in enumerate(segments):
		print(f"Translating segment {i+1} of {len(segments)}...")
		translated_text += translator.translate(segment, dest=dest_language).text

	return translated_text

def google_text_to_speech(text, language, output_file):
	from gtts import gTTS
	tts = gTTS(text=text, lang=language)
	tts.save(output_file)

def get_language_code(engine):
	languages = get_available_languages_googletrans()
	print("\nChoose language audio source:")
	user_input = input()
	language = process.extractOne(user_input, languages)[0]
	language_name = language.lower()
	for code, name in LANGUAGES.items():
		if name == language_name:
			clear_screen()
			sys.stdout.write(f"Audio: {wav.capitalize()}\nEngine: {engine.capitalize()}\nAudio Language: {language_name.capitalize()} - {code.capitalize()}")
			sys.stdout.flush()
			return code
	return None

def choose_language(engine,audio_language):
	languages = get_available_languages_googletrans()
	print("\nChoose a language to text-to-speech :")
	user_input = input('[Press 0 Back] : ')
	if user_input == '0':
		return None
	language = process.extractOne(user_input, languages)[0]
	clear_screen()
	sys.stdout.write(f"Audio: {wav.capitalize()}\nEngine: {engine.capitalize()}\nAudio Language: {audio_language}\nTo Language: {language.capitalize()}")
	sys.stdout.flush()
	return language

def get_available_languages_googletrans():
	return set(LANGUAGES.values())

def menu1(engin,audio_language):
	global language
	language = choose_language(engine_choice,audio_language)

def start():
	global engine_choice
	global audio_language
	clear_screen()
	engine_choice = set_engine('Google')
	audio_language = get_language_code(engine_choice)
	menu1(engine_choice,audio_language)
	if language is None:
		start()

start()

sys.stdout.write("\nStarting transcription...")
sys.stdout.flush()
transcribe_text = transcribe_audio_to_text(f'{wav}',audio_language)

sys.stdout.write("\rTranscription completed.                         ")
sys.stdout.flush()
sys.stdout.write("\033[F") 

sys.stdout.write("\rStarting translation...")
sys.stdout.flush()
transcribe_text = translate_text(transcribe_text, language)
sys.stdout.write("\033[F")
sys.stdout.write("\rTranslation completed.                         ")
sys.stdout.flush()

sys.stdout.write("\nStarting text to speech conversion...")
sys.stdout.flush()
if engine_choice == '1':
	google_text_to_speech(transcribe_text, language, f'{language}_audio.mp3')
sys.stdout.write("\033[F")
sys.stdout.write("\rText to speech conversion completed.                         ")
sys.stdout.flush()
sys.stdout.write("\033[F")
print(f"\n{language.capitalize()} audio saved as {language}_audio.mp3")