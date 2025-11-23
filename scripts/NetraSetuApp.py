# AI disclosure: few parts of code made with assistance from GPT-5 mini
import flet as ft
import threading
import queue
import speech_recognition as sr
import pyttsx3
from NetraSetu import texttobraille, summary, report, mindmap
from VoiceAI import genchat
# flag to ensure genchat is started only once
assistant_thread_started = False
# ----------------------------
# Voice Assistant Setup
# ----------------------------
engine = pyttsx3.init()
recognizer = sr.Recognizer()
tts_queue = queue.Queue()

# Single background TTS thread
def tts_worker():
    while True:
        text = tts_queue.get()
        engine.say(text)
        engine.runAndWait()
        tts_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def speak(text):
    tts_queue.put(text)

# Execute voice commands
def execute_command(command, page: ft.Page):
    cmd = command.lower()
    response = ""

    if "home" in cmd:
        page.go("/")
        response = "Navigating to home"
    elif "braille" in cmd:
        page.go("/braille")
        response = "Opening Braille Converter"
    elif "assistant" in cmd:
        page.go("/assistant")
        response = "Opening AI Assistant"
    elif "learning hub" in cmd:
        page.go("/learning")
        response = "Opening Learning Hub"
    elif "summary" in cmd:
        page.go("/summary")
        response = "Opening Summary Generator"
    elif "report" in cmd:
        page.go("/report")
        response = "Opening Report Generator"
    elif "mind map" in cmd or "mindmap" in cmd:
        page.go("/mindmap")
        response = "Opening Mind Map Generator"
    elif "back" in cmd:
        page.go("/")
        response = "Going back"
    else:
        response = "Command not recognized"

    speak(response)

# Continuous listening
def listen_continuously(page: ft.Page):
    def background_listener():
        with sr.Microphone() as source:
            speak("Voice assistant is now listening")
            while True:
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print("Voice Command:", command)
                    execute_command(command, page)
                except (sr.WaitTimeoutError, sr.UnknownValueError):
                    continue
                except sr.RequestError:
                    speak("Speech service unavailable")
    threading.Thread(target=background_listener, daemon=True).start()

# ----------------------------
# Pages
# ----------------------------

def home_page(page: ft.Page, uploaded_text: ft.Text):
    # FilePicker
    def upload_file(e: ft.FilePickerResultEvent):
        file_name = "my_document.txt"
        a = e.files[0].path
        # read the uploaded file contents (keep original text)
        with open(a, 'r', encoding="utf-8") as f:
            d = f.read()
        # store the original extracted text in the uploaded_text control
        uploaded_text.value = d
        # also write the original text to a local file for persistence
        with open(file_name, 'w', encoding="utf-8") as file:
            file.write(d)
        # clear previously generated outputs so they will be overwritten on next generation
        for fn in ("summary.txt", "report.txt", "mindmap.txt"):
            try:
                with open(fn, 'w', encoding="utf-8") as _f:
                    _f.write("")
            except Exception:
                pass
        page.update()
        

    file_picker = ft.FilePicker(on_result=upload_file)
    page.overlay.append(file_picker)

    return ft.View(
        route="/",
        controls=[
            ft.Column([
                ft.Text("NetraSetu", size=40, weight="bold", color=ft.Colors.BLUE_800),
                ft.Divider(thickness=2, color=ft.Colors.BLUE_200),
                ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton("Braille Converter", width=250, height=50, on_click=lambda _: page.go("/braille")),
                        ft.ElevatedButton("AI Assistant", width=250, height=50, on_click=lambda _: page.go("/assistant")),
                        ft.ElevatedButton("Learning Hub", width=250, height=50, on_click=lambda _: page.go("/learning")),
                        ft.ElevatedButton("Upload Document", width=250, height=50, on_click=lambda _: file_picker.pick_files())
                    ], spacing=20),
                    padding=20,
                    bgcolor="#f0f8ff",
                    border_radius=10
                ),
                uploaded_text,
                ft.Text("© NetraSetu 2025", size=14, color=ft.Colors.GREY_600)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

def braille_page(page: ft.Page, uploaded_text: ft.Text):
    # generate braille preview from the uploaded text value
    text_value = uploaded_text.value or ""
    braille_preview = ft.Text(texttobraille(text_value.lower()), size=20)
    file_name = "my_document.txt"
    text=braille_preview.value
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(text)

    return ft.View(
        route="/braille",
        controls=[
            ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))]),
                ft.Text("Braille Converter", size=32, weight="bold"),
                ft.Divider(thickness=2),
                ft.Text("Uploaded Text:"),
                uploaded_text,
                ft.Text("Braille Preview:"),
                ft.Container(content=braille_preview, padding=10, bgcolor="#000000"),
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.START)
        ],
        padding=20
    )

def ai_assistant_page(page: ft.Page):
    # Instruction text — genchat uses the keyboard space key to record
    instruction = ft.Text("Hold SPACE to talk. Press SPACE to start recording.", size=16, color=ft.Colors.GREY_700)

    # start genchat in a background thread when the assistant page is created
    global assistant_thread_started
    if not assistant_thread_started:
        threading.Thread(target=genchat, daemon=True).start()
        assistant_thread_started = True

    return ft.View(
        route="/assistant",
        controls=[
            ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))]),
                ft.Text("AI Assistant", size=36, weight="bold"),
                ft.Divider(thickness=2),
                ft.Row([instruction], alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=20)
        ],
        padding=30
    )

def learning_hub(page: ft.Page):
    return ft.View(
        route="/learning",
        controls=[
            ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/"))]),
                ft.Text("Learning Hub", size=36, weight="bold"),
                ft.Divider(thickness=2),
                ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton("Summary Generator", width=250, height=50, on_click=lambda _: page.go("/summary")),
                        ft.ElevatedButton("Report Generator", width=250, height=50, on_click=lambda _: page.go("/report")),
                        ft.ElevatedButton("Mind Map", width=250, height=50, on_click=lambda _: page.go("/mindmap")),
                    ], spacing=20),
                    padding=20,
                    bgcolor="#f9f9f9",
                    border_radius=10
                )
            ], spacing=30)
        ],
        padding=20
    )
def summary_page(page: ft.Page, uploaded_text: ft.Text):
    # Use uploaded_text.value as source; don't show the full input in the UI
    result_field = ft.TextField(label="Summary", multiline=True, min_lines=6, read_only=True)
    loader = ft.ProgressRing(visible=False)

    def generate_summary(e):
        # no visible input - use uploaded_text.value as the source
        text_source = uploaded_text.value if uploaded_text.value and uploaded_text.value != "No document uploaded yet." else ""
        if not text_source:
            result_field.value = "No uploaded document to summarize."
            page.update()
            return

        loader.visible = True
        page.update()

        def work():
            try:
                res = summary(text_source)
            except Exception as ex:
                res = f"Error generating summary: {ex}"
            result_field.value = res
            # convert to braille and save to file so it can be overwritten on next upload
            try:
                braille_out = texttobraille(res.lower())
                with open('summary.txt', 'w', encoding='utf-8') as f:
                    f.write(braille_out)
            except Exception:
                pass
            loader.visible = False
            page.update()

        threading.Thread(target=work, daemon=True).start()

    # Auto-run summary on page render if uploaded text exists
    page.after_render = lambda _: (generate_summary(None) if uploaded_text.value and uploaded_text.value != "No document uploaded yet." else None)

    return ft.View(
        route="/summary",
        controls=[
            ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/learning"))]),
                ft.Text("Summary Generator", size=32, weight="bold"),
                ft.Divider(thickness=2),
                ft.Row([ft.ElevatedButton("Generate Summary", on_click=generate_summary), loader]),
                result_field
            ], spacing=16)
        ],
        padding=20
    )


def report_page(page: ft.Page, uploaded_text: ft.Text):
    result_field = ft.TextField(label="Report", multiline=True, min_lines=8, read_only=True)
    loader = ft.ProgressRing(visible=False)

    def generate_report(e):
        text_source = uploaded_text.value if uploaded_text.value and uploaded_text.value != "No document uploaded yet." else ""
        if not text_source:
            result_field.value = "No uploaded document to generate a report from."
            page.update()
            return

        loader.visible = True
        page.update()

        def work():
            try:
                res = report(text_source)
            except Exception as ex:
                res = f"Error generating report: {ex}"
            result_field.value = res
            # convert to braille and save to file so it can be overwritten on next upload
            try:
                braille_out = texttobraille(res.lower())
                with open('report.txt', 'w', encoding='utf-8') as f:
                    f.write(braille_out)
            except Exception:
                pass
            loader.visible = False
            page.update()

        threading.Thread(target=work, daemon=True).start()

    # Auto-run report on page render if uploaded text exists
    page.after_render = lambda _: (generate_report(None) if uploaded_text.value and uploaded_text.value != "No document uploaded yet." else None)

    return ft.View(
        route="/report",
        controls=[
            ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/learning"))]),
                ft.Text("Report Generator", size=32, weight="bold"),
                ft.Divider(thickness=2),
                ft.Row([ft.ElevatedButton("Generate Report", on_click=generate_report), loader]),
                result_field
            ], spacing=16)
        ],
        padding=20
    )


def mindmap_page(page: ft.Page, uploaded_text: ft.Text):
    result_field = ft.TextField(label="Mind Map Outline", multiline=True, min_lines=8, read_only=True)
    loader = ft.ProgressRing(visible=False)

    def generate_mindmap(e):
        text_source = uploaded_text.value if uploaded_text.value and uploaded_text.value != "No document uploaded yet." else ""
        if not text_source:
            result_field.value = "No uploaded document to create a mind map from."
            page.update()
            return

        loader.visible = True
        page.update()

        def work():
            try:
                res = mindmap(text_source)
            except Exception as ex:
                res = f"Error generating mind map: {ex}"
            result_field.value = res
            # convert to braille and save to file so it can be overwritten on next upload
            try:
                braille_out = texttobraille(res.lower())
                with open('mindmap.txt', 'w', encoding='utf-8') as f:
                    f.write(braille_out)
            except Exception:
                pass
            loader.visible = False
            page.update()

        threading.Thread(target=work, daemon=True).start()

    # Auto-run mindmap on page render if uploaded text exists
    page.after_render = lambda _: (generate_mindmap(None) if uploaded_text.value and uploaded_text.value != "No document uploaded yet." else None)

    return ft.View(
        route="/mindmap",
        controls=[
            ft.Column([
                ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/learning"))]),
                ft.Text("Mind Map Generator", size=32, weight="bold"),
                ft.Divider(thickness=2),
                ft.Row([ft.ElevatedButton("Generate Mind Map", on_click=generate_mindmap), loader]),
                result_field
            ], spacing=16)
        ],
        padding=20
    )

# ----------------------------
# App Router
# ----------------------------
def main(page: ft.Page):
    listen_continuously(page)
    uploaded_text = ft.Text("No document uploaded yet.", size=16)

    def route_change(e):
        page.views.clear()
        routes = {
            "/": home_page(page, uploaded_text),
            "/braille": braille_page(page, uploaded_text),
            "/assistant": ai_assistant_page(page),
            "/learning": learning_hub(page),
            "/summary": summary_page(page, uploaded_text),
            "/report": report_page(page, uploaded_text),
            "/mindmap": mindmap_page(page, uploaded_text),
        }
        page.views.append(routes.get(e.route, home_page(page, uploaded_text)))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)