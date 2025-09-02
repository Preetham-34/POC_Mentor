import io
from gtts import gTTS
import streamlit as st

def speak(text: str):
    tts = gTTS(text=text, lang="en")
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    st.audio(buf.getvalue(), format="audio/mp3")
