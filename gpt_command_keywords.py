import pyperclip
import time
import pyttsx3

# Speech engine setup
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')

def speak(text):
    engine.say(text)
    engine.runAndWait()


# Clipboard Commands
def get_from_clipboard():
    speak("Copying the code from your clipboard now.")
    time.sleep(3)
    content = pyperclip.paste()
    return content

def copy_to_clipboard(gpt_text):
    if "```" in gpt_text:
        code_to_copy = gpt_text.split("```")
        pyperclip.copy(code_to_copy[1])
    else:
        pyperclip.copy(gpt_text)