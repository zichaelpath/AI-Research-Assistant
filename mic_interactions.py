import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play


r = sr.Recognizer()

def record_audio_keyword():
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=6)
    audio_segment = AudioSegment(
        data=audio_data.get_wav_data(),
        sample_width=2,
        frame_rate=44100,
        channels=1
    )
    audio_segment.export('keyword.wav', format='wav')


def record_audio_prompt():
    audio_data = None
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=10)
    audio_segment = AudioSegment(
        data=audio_data.get_wav_data(),
        sample_width=2,
        frame_rate=44100,
        channels=1
    )
    audio_segment.export('output.wav', format='wav')