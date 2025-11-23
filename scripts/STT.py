import speech_recognition as sr
import keyboard
from enum import Enum
import time

class Language(Enum):
    ENGLISH = "en-US"
    HINDI = "hi-IN"

def speech_to_text(device_index, language=Language.HINDI):
    r = sr.Recognizer()
    print("Hold SPACE to talk...")
    keyboard.wait("space")
    print("Recording... Keep holding SPACE")
    with sr.Microphone(device_index=device_index) as source:
        r.adjust_for_ambient_noise(source)
        frames = []
        start_time = time.time()
        while keyboard.is_pressed("space"):
            audio = source.stream.read(4096)
            frames.append(audio)
        print("Stopped recording")
    audio_data = sr.AudioData(b"".join(frames), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
    print("Processing...")

    try:
        text = r.recognize_google(audio_data, language=language.value)
        # print("You said:", text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    speech_to_text(device_index=1)
