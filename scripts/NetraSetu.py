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
    response = ollama.chat(model="gemma3:1b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def report(text: str) -> str:
    prompt = f"Generate a detailed report based on the following information:\n\n{text}\n\nReport:"
    response = ollama.chat(model="gemma3:1b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def mindmap(text: str) -> str:
    prompt = f"Create a mind map outline based on the following content in a form like this XXXXXXXXX -----------------XXXXXXXX:\n\n{text}\n\nMind Map:"
    response = ollama.chat(model="gemma3:1b", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

