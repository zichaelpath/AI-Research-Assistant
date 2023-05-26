import sounddevice as sd
import soundfile as sf
import PySimpleGUI as sg
import openai
import numpy as np
from gpt_command_keywords import *
from mic_interactions import *
import pyperclip
import time
with open('key.txt', 'r') as key:
    ky = key.read()
    openai.api_key = ky

# Audio recording parameters
fs = 44100  # Sample rate
channels = 1  # We're using mono audio for simplicity
duration = 20  # Maximum duration in seconds
recording = None  # The recording buffer

r = sr.Recognizer()


messages = [{"role": "system", "content": "You are a research assistant helping me with my programming and anything else I require."}]

keyword_collection = ['yes', 'no', 'hey gpt', 'clipboard', 'exit']

def append_messages(role, prompt):
    message_template = {"role": role, "content": prompt}
    messages.append(message_template)


# This flag will indicate whether we're currently recording
is_recording = False
use_clip = None
analyse_code = False
clip_content = None
gpt_text = ""
no_resp = None
help_quest = None
exit_loop = None


def play_sound(play_s):
    sound = AudioSegment.from_file(play_s, format="wav")
    play(sound)




def clipboard_functionality(text):
    global clip_content, analyse_code
    speak("Would you like to copy to your clipboard or to copy from your clipboard?")
    record_audio_keyword()
    audio_file = open('keyword.wav', 'rb')
    result = openai.Audio.transcribe('whisper-1', audio_file)
    check = result['text']
    if 'copy to my clipboard' in check.lower():
        copy_to_clipboard(text)
        speak("The code has been copied to your clipboard.")
    elif 'from my clipboard' in check.lower():
        clip_content = get_from_clipboard()
        analyse_code = True


def code_analysis(content):
    prompt = f"I have some code that I am having trouble with and I need your help to solve it. This is my code \n {content}.\n"
    speak('Please tell me what you are trying to do.')
    record_audio_prompt()
    audio_file = open('output.wav', 'rb')
    speak('Thank you, transcribing now.')
    transcribe = openai.Audio.transcribe('whisper-1', audio_file)
    prompt += transcribe["text"]
    append_messages("user", prompt)
    speak("Transcribed audio, prompting GPT")
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    ana_gpt = completion["choices"][0]["message"]["content"]
    speak(ana_gpt)


def is_audio_silent():
    audio_file = open('keyword.wav', 'rb')
    result = openai.Audio.transcribe('whisper-1', audio_file)
    transcript = result['text'].lower() if result else ''
    return transcript == ''


def check_for_keyword():
    audio_file = open('keyword.wav', 'rb')
    result = openai.Audio.transcribe('whisper-1', audio_file)
    transcript = result['text'].lower() if result else ''

    if not transcript:
        return False, True, False, False

    keyword_present = {keyword: keyword in transcript for keyword in keyword_collection}

    if keyword_present['hey gpt'] or keyword_present['yes']:
        return True, False, False, False
    elif keyword_present['no']:
        return False, False, True, False
    elif keyword_present['clipboard']:
        return True, False, False, False
    elif keyword_present['exit']:
        return False, False, False, True
    else:
        return False, False, False, False


welcome_message = 'Hello, I am a prompt based research assistant. I am here to assist you with all your coding and general question needs.\n'\
                + 'When I am first ran, you will have to say the keyword \'Hey GPT\' to get started. I will vocally guide you to say your search term.\n'\
                + 'My creator hs given me a time of 30 seconds for you to speak your prompt, buy please don\'t speak too fast or I may not understand.\n'\
                + 'Finally, after every prompt I will ask you to prompt again. You can choose Yes or No. If you choose Yes, I will prompt you again to speak.\n'\
                + 'If you choose No, I will go back to listening until the next time you say the keyword. Feel free to minimize me, but be mindful of the pop up to speak again.'\
                + 'Also, before you can use me, you will have to put in your OpenAi API key that you can get on their developer website. \nStore this file in the same folder as your application\n and name it \'key.txt\'.'

input_time = 'Please type the time, in seconds, that you wish me to record your prompt. Note that I will record for the full length'

# Create a new PySimpleGUI window
layout = [[sg.Text(welcome_message)], [sg.Button('Exit', key='exit')]]
window = sg.Window('Recorder', layout, return_keyboard_events=True)





def talk_gpt():
    global gpt_text
    speak("Record your prompt now")
    record_audio_prompt()
    audio_file = open('output.wav', 'rb')
    transcribe = openai.Audio.transcribe('whisper-1', audio_file)
    prompt = transcribe["text"]
    print(prompt)
    append_messages("user", prompt)
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    text = completion["choices"][0]["message"]["content"]
    speak(text)
    gpt_text = text


prompt_again = True
loop_counter = 0
response = None
# The event loop
while True:
    event, values = window.read(timeout=100)

    if not prompt_again:
        break

    if event == 'exit':
        break

    record_audio_keyword()
    prompt_audio = None
    gpt_prompt = None
    use_clip, no_resp, help_quest, exit_loop = check_for_keyword()
    if not is_audio_silent() and not exit_loop:
        talk_gpt()
        if use_clip:
            clipboard_functionality(gpt_text)
        if analyse_code:
            code_analysis(clip_content)
        if not response:
            continue
        if event == sg.WINDOW_CLOSED or event == 'Escape':
            break
    use_clip, no_resp, help_quest, exit_loop, analyse_code = False
    if exit_loop:
        speak("Have a nice afternoon Mr Shade")
        break

window.close()

