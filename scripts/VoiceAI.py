import ollama
import edge_tts
import asyncio
import speech_recognition as sr
import keyboard
from enum import Enum
import time
from playsound import playsound

def genchat():
    class Language(Enum):
        ENGLISH = "en-US"
        HINDI = "hi-IN"

    def speech_to_text(device_index, language=Language.ENGLISH):
        r = sr.Recognizer()
        print("Hold SPACE to talk...")
        keyboard.wait("space")
        print("Recording... Keep holding SPACE")
        frames = []
        txt_out = ""
        with sr.Microphone(device_index=device_index) as source:
            r.adjust_for_ambient_noise(source)
            while keyboard.is_pressed("space"):
                try:
                    audio = r.listen(source, phrase_time_limit=1)
                    frames.append(audio)
                except:
                    break

        print("Stopped recording")
        print("Processing...")

        if len(frames) == 0:
            return ""

        combined_raw = b"".join([f.get_raw_data() for f in frames])
        sample_rate = frames[0].sample_rate
        sample_width = frames[0].sample_width
        audio_data = sr.AudioData(combined_raw, sample_rate, sample_width)

        try:
            txt_out = r.recognize_google(audio_data, language=language.value)
        except:
            txt_out = ""

        return txt_out
    history = []

    while True:
        user_input = speech_to_text(device_index=1)

        if user_input == "":
            print("(no speech detected)")
            continue

        print("You said:", user_input)

        if user_input.lower() in ["exit", "quit", "bye", "stop"]:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        print("AI: ", end="", flush=True)
        assistant_reply = ""

        stream = ollama.chat(
            model="gemma3:1b",
            messages=history,
            stream=True
        )

        for chunk in stream:
            part = chunk["message"]["content"]
            assistant_reply += part
            print(part, end="", flush=True)

        print()

        history.append({"role": "assistant", "content": assistant_reply})

        async def run_tts():
            tts = edge_tts.Communicate(assistant_reply, "en-IN-NeerjaNeural")
    
            with open("test.mp3", "wb") as f:
                async for chunk in tts.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
        asyncio.run(run_tts())
        playsound("test.mp3")
    
    

# if __name__ == "__main__":
#     genchat()
