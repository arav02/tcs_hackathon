# speech_utils.py (No changes needed from the original post)

import io
from gtts import gTTS
import os
from streamlit_mic_recorder import mic_recorder
from speech_recognition import Recognizer, AudioFile

def get_audio_bytes_for_streamlit(text: str, lang: str = 'en') -> bytes:
    """
    Converts text to speech using the free gTTS API and returns the audio content as bytes.
    """
    try:
        # gTTS interfaces with the free Google Translate TTS API
        tts = gTTS(text=text, lang=lang)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        audio_bytes = audio_fp.read()
        return audio_bytes
    except Exception as e:
        print(f"Error generating audio bytes with gTTS: {e}")
        return b''
    
    
def convert_audio_to_text(audio_bytes):
    """
    Converts speech audio bytes to text using the free Google Web Speech API.
    """

    if not audio_bytes:
        return None
        
    temp_filename = "temp_audio.wav"
    try:
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)
            
        r = Recognizer()
        with AudioFile(temp_filename) as source:
            r.adjust_for_ambient_noise(source) 
            audio = r.record(source) 

        # This uses the FREE Google Web Speech API (no key required)
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        # st.error(f"STT Error: Could not request results from Google Speech Recognition service; {e}")
        return "Could not understand audio. (Requires internet connection)"
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)