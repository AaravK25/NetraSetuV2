import ollama
import edge_tts
import asyncio
import pdfplumber

def textPDF(pathPDF):
    with pdfplumber.open(pathPDF) as pdf, open("output.txt", "w", encoding="utf-8") as f:
    
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                f.write(t + '\n')
    b = str(input("Enter PDF file: "))
    textPDF(b)


def texttobraille(input_str: str):
    # Source - https://stackoverflow.com/a
    # Posted by HumpbackWhale194
    # Retrieved 2025-11-22, License - CC BY-SA 4.0

    mapping = {
     ' ': '⠀',
     '!': '⠮',
     '"': '⠐',
     '#': '⠼',
     '$': '⠫',
     '%': '⠩',
     '&': '⠯',
     "'": '⠄',
     '(': '⠷',
     ')': '⠾',
     '*': '⠡',
     '+': '⠬',
     ',': '⠠',
     '-': '⠤',
     '.': '⠨',
     '/': '⠌',
     '0': '⠴',
     '1': '⠂',
     '2': '⠆',
     '3': '⠒',
     '4': '⠲',
     '5': '⠢',
     '6': '⠖',
     '7': '⠶',
     '8': '⠦',
     '9': '⠔',
     ':': '⠱',
     ';': '⠰',
     '<': '⠣',
     '=': '⠿',
     '>': '⠜',
     '?': '⠹',
     '@': '⠈',
     'a': '⠁',
     'b': '⠃',
     'c': '⠉',
     'd': '⠙',
     'e': '⠑',
     'f': '⠋',
     'g': '⠛',
     'h': '⠓',
     'i': '⠊',
     'j': '⠚',
     'k': '⠅',
     'l': '⠇',
     'm': '⠍',
     'n': '⠝',
     'o': '⠕',
     'p': '⠏',
     'q': '⠟',
     'r': '⠗',
     's': '⠎',
     't': '⠞',
     'u': '⠥',
     'v': '⠧',
     'w': '⠺',
     'x': '⠭',
     'y': '⠽',
     'z': '⠵',
     '[': '⠪',
     '\\': '⠳',
     ']': '⠻',
     '^': '⠘',
     '_': '⠸',
     '•': ' ',
     '\n': '\n'
     }
    

    def convert_str(input_str: str) -> str:
        out = ""
        for input_char in input_str:
            # fall back to the original character if no mapping is found
            out += mapping.get(input_char, input_char)
        return out
    return convert_str(input_str)

# this thing helps in writing braille text to a file, basically it is the braille converting part
# file_name = "my_document.txt"
# a = str(input("file:")).lower()
# c = open(a)
# d=c.read().lower()
# text=texttobraille(d)
# with open(file_name, 'w', encoding="utf-8") as file:
#         file.write(text)



# async def main():
#     tts = edge_tts.Communicate(text, "en-IN-PrabhatNeural") #ml-IN-MidhunNeural, kn-IN-GaganNeural, hi-IN-MadhurNeural, ta-IN-ValluvarNeural
#     await tts.save("test.mp3")

# asyncio.run(main())

def summary(text: str) -> str:
    prompt = f"Summarize the following text in a concise manner:\n\n{text}\n\nSummary:"
    response = ollama.chat(model="gemma3:4b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def report(text: str) -> str:
    prompt = f"Generate a detailed report based on the following information for a student:\n\n{text}\n\nReport:"
    response = ollama.chat(model="gemma3:4b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def mindmap(text: str) -> str:
    prompt = (
        "Create a clean mind map outline from the following content.\n"
        "Use THIS EXACT STRUCTURE:\n\n"
        "Title 1\n"
        "|\n"
        "|\n"
        "|---- Subtopic 1\n"
        "|       1.Point 1 ; 2.point 2\n"  
        "|\n"
        "Title 2\n"
        "|\n"
        "|\n"
        "|---- Subtopic 2\n\n"
        "|       1.Point 1 ; 2.point 2\n\n"
        "Rules:\n"
        "- Each title must be on its own line.\n"
        "- After each title, add two vertical '|' lines.\n"
        "- For each title, list its subtopics using: |---- <subtopic>\n"
        "- Under each subtopic, list points as numbered items separated by semicolons.\n"
        "- Add a '|' line between each major block.\n"
        "- Keep the formatting exactly as shown.\n\n"
        f"Content:\n{text}\n\n"
        "Mind Map:"
    )

    response = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


