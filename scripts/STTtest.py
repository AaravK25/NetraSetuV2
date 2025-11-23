import speech_recognition as sr
from enum import Enum
import keyboard

time = float(input("Enter the time limit for speech recognition (in seconds): "))

class Language(Enum):
    ENGLISH = "en-US"
    CHINESE = "zh-CN"
    HINDI = "hi-IN"
    MALAYALAM = "ml-IN"
    TAMIL = "ta-IN"
    KANNADA = "kn-IN"
    FRENCH = "fr-FR"
    KOREAN = "ko-KR"
    JAPANESE = "ja-JP"

class SpeechToText():
    def print_mic_device_index():
        for index,name in enumerate(sr.Microphone.list_microphone_names()):
            print("{1}, devices_index={0}".format(index,name))

    def speech_to_text(device_index, language=Language.ENGLISH):
        r = sr.Recognizer()
        with sr.Microphone(device_index=device_index) as source:
            print("Start Talking:")
            audio = r.listen(source, phrase_time_limit=time)
            try:
                text = r.recognize_google(audio, language=language.value)
                print("You said: {}".format(text))
            except:
                print("Please try again.")

def check_mic_device_index():
    SpeechToText.print_mic_device_index()
    
def run_speech_to_text_english(device_index):
    SpeechToText.speech_to_text(device_index=device_index)

def run_speech_to_text_malayalam(device_index):
    SpeechToText.speech_to_text(device_index=device_index, language=Language.MALAYALAM)

def run_speech_to_text_hindi(device_index):
    SpeechToText.speech_to_text(device_index=device_index, language=Language.HINDI)

def run_speech_to_text_chinese(device_index,language):
    SpeechToText.speech_to_text(device_index,language)

if __name__ == "__main__":
    # check_mic_device_index()
    run_speech_to_text_english(device_index=1)
    # run_speech_to_text_hindi(device_index=1)
    # run_speech_to_text_malayalam(device_index=1)