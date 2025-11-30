# NetraSetu
This project was made during the Synthax Hackathon. It can be used for visually impaired students with the help of their teachers.

Topic – Inclusive Learning for All

Problem Statement:
The Indian constitution provides its citizens the Right to Education which guarantees free and compulsory education for children from 6 to 14 years of age in government schools and it also mandates inclusive education for children with disabilities, including those who are visually impaired however due to lack of proper enforcement and inadequate training for the teachers they are not able to support the visually impaired students properly. This indirectly affects the economy since they are not able to provide a valuable contribution due to lack of education. This population need not be a liability. It can be turned into a productive asset by investment in human capital to increase their productivity and develop their skills.
Non-existence of educational platforms/informational systems; not driven by the existing technology stack to enable the deprived class to be more productive and empowering the teachers to make them more inclusive.

Solution:
NetraSetu an app consisting of a smart AI voice assistant, braille converting software and compatibility for English language will help in breaking this educational gap for the visually impaired students. The app will have a minimalistic design to ensure easy understanding of the features. The user is expected to provide the app necessary source to extract the information from.


Features:-

•	Smart AI voice Assistant. The student can navigate through the App using this assistant reducing dependence on teacher.

•	Text To Braille feature where text will be converted to Braille using Unicode Braille System. English to braille conversion will be there.

•	Braille Mind maps will be generated using AI

•	It will also have the feature of converting the sources into summarized braille docs.

•	The AI voice assistant can solve the child’s queries reducing constant dependence on the teacher.

*NOTE: The braille documents are not in braille ASCII

Conclusion:
The current teaching process is person dependant , so the actual knowledge transfer cannot be quantified and there is no inclusivity being adhered
The product would be demo’d to the schools  to get the actual buy in. Based on the scalability of the product deployment  the investors as corporates would be engaged with  the help of NGO/government grant accordingly. Training camps would be organized  to set the expectations  for the teachers  so that  the real benefit would pass on  to the students.
  
## Tech stack
- Python (project code in scripts/*.py)
- Flet for UI (single-file app UI + router) — main UI in NetraSetuApp.main and view factories: NetraSetuApp.home_page, NetraSetuApp.braille_page, NetraSetuApp.ai_assistant_page, NetraSetuApp.learning_hub, NetraSetuApp.summary_page, NetraSetuApp.report_page, NetraSetuApp.mindmap_page
- Speech recognition: SpeechRecognition library (uses Google recognizer by default) — continuous listening in NetraSetuApp.listen_continuously and STT helpers in STT.speech_to_text / STTtest
- Text-to-speech: local queue with pyttsx3 (background thread NetraSetuApp.tts_worker) and optional Edge TTS in [NetraSetu.summary / VoiceAI usage](scripts/NetraSetu.py) / [VoiceAI.genchat](scripts/VoiceAI.py)
- Local LLM calls via Ollama in NetraSetu.summary, NetraSetu.report, NetraSetu.mindmap and chat in VoiceAI.genchat
- PDF extraction via pdfplumber (NetraSetu.py) (not using)
- Braille conversion utility: NetraSetu.texttobraille
- Other utilities: playsound, keyboard

## Architecture (high level)
- Single-process Python app with threads:
  - UI layer: Flet view router backed by NetraSetuApp.main
  - Background TTS worker: NetraSetuApp.tts_worker + tts_queue and exposed helper NetraSetuApp.speak
  - Background continuous speech listener: NetraSetuApp.listen_continuously → recognizes commands and routes via NetraSetuApp.execute_command
  - AI workers: synchronous calls to Ollama in NetraSetu.summary, NetraSetu.report, NetraSetu.mindmap invoked from page worker threads in the UI pages
  - Optional chat assistant: VoiceAI.genchat run in its own daemon thread when assistant page is opened
- File storage for persistent outputs:
  - Uploaded source saved to my_document.txt
  - Generated braille outputs written to summary.txt, report.txt, mindmap.txt
- Key modules / entrypoints:
  - app UI and router: NetraSetuApp.main — file: NetraSetuApp.py
  - braille / generation logic: NetraSetu.py : NetraSetu.texttobraille, NetraSetu.summary, NetraSetu.report, NetraSetu.mindmap
  - voice assistant chat: VoiceAI.py — VoiceAI.genchat
  - STT helpers/test: STT.py, STTtest.py

## Quick setup 

1. Install Python 3.10+ and create a virtual environment
2. install common dependencies
pip install flet pyttsx3 SpeechRecognition keyboard playsound ollama edge-tts pyaudio 


## Run the app NetraSetuApp.py
- This launches the Flet app which calls [NetraSetuApp.main](scripts/NetraSetuApp.py) and starts background listeners/threads.

## Notes & operational details
- Ollama: the project calls Ollama locally in [NetraSetu.summary](scripts/NetraSetu.py) and [VoiceAI.genchat](scripts/VoiceAI.py). Ensure an Ollama service/model (gemma3:1b) is available and accessible.
- Microphone permissions: the continuous listener uses the default microphone in [NetraSetuApp.listen_continuously](scripts/NetraSetuApp.py). Provide OS microphone permission and confirm device indices using STT test scripts ([scripts/STTtest.py](scripts/STTtest.py)).
- Braille conversion: use [NetraSetu.texttobraille](scripts/NetraSetu.py) — generated outputs are written to [summary.txt](summary.txt), [report.txt](report.txt), [mindmap.txt](mindmap.txt)
- Assistant chat: [VoiceAI.genchat](scripts/VoiceAI.py) uses keyboard-based recording (hold SPACE) and streams TTS via edge-tts; run in background thread via [NetraSetuApp.ai_assistant_page](scripts/NetraSetuApp.py)
- File paths: uploaded files are written to [my_document.txt](my_document.txt) by the upload handler in [NetraSetuApp.home_page](scripts/NetraSetuApp.py)

## Files referenced
- [scripts/NetraSetuApp.py](scripts/NetraSetuApp.py)
- [scripts/NetraSetu.py](scripts/NetraSetu.py)
- [scripts/VoiceAI.py](scripts/VoiceAI.py)
- [scripts/STT.py](scripts/STT.py)
- [scripts/STTtest.py](scripts/STTtest.py)
- [my_document.txt](my_document.txt)
- [summary.txt](summary.txt)
- [mindmap.txt](mindmap.txt)
- [report.txt](report.txt)

## Division of work:

-Back - end: Aarav Koul, Unicode Braille System, Speech Recognition, Edge-TTS, Ollama.

-front - end: Aniruddha Sahoo, Adithya Vivek, flet, pyttsx3, speech recognition.

DISCLOSURES: GitHub Copilot (GPT-5 mini) used for debugging and assistance in front-end and implentation of features from scripts NetraSetu.py and VoiceAI.py

## License

This project is licensed under the BSD 3-Clause License. Attribution is required.

Please credit: Aarav Koul, Aniruddha Sahoo, and Adithya Vivek.
