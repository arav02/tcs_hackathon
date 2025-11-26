# app.py (No changes needed from the original post)

import streamlit as st
import os
# Imports the free TTS function from the module
from speech_utils import get_audio_bytes_for_streamlit 
from streamlit_mic_recorder import mic_recorder
from speech_utils import convert_audio_to_text
from speech_recognition import Recognizer, AudioFile

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Free Speech Functions Demo")


st.title("🗣️ Free Speech Utilities Demo (No Subscription)")

# --- Speech-to-Text Section ---
st.header("1. Speech to Text (STT) - Requires Internet")

audio_data = mic_recorder(
    start_prompt="Record",
    stop_prompt="Stop",
    key='mic_recorder',
    format="wav"
)

if audio_data and 'bytes' in audio_data:
    st.session_state.transcribed_text = convert_audio_to_text(audio_data['bytes'])
    
if 'transcribed_text' in st.session_state and st.session_state.transcribed_text is not None:
    st.subheader("Transcription:")
    st.info(st.session_state.transcribed_text)
    
st.markdown("---")

# --- Text-to-Speech Section ---
st.header("2. Text to Speech (TTS) - Requires Internet")

tts_text = st.text_area(
    "Enter text to convert to speech:",
    "This uses the free gTTS library for clear, natural speech, with no subscription required.",
    height=150
)

if st.button("Generate & Play Speech 🔊"):
    if tts_text:
        with st.spinner('Generating speech...'):
            audio_bytes = get_audio_bytes_for_streamlit(tts_text)
            
        if audio_bytes:
            st.subheader("Playback:")
            st.audio(audio_bytes, format='audio/mp3')
            st.download_button(
                label="Download MP3",
                data=audio_bytes,
                file_name="generated_speech.mp3",
                mime="audio/mp3"
            )
        else:
            st.error("Failed to generate audio. Check the text input.")
    else:
        st.warning("Please enter some text for TTS conversion.")