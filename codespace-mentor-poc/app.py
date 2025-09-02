import json
import streamlit as st
from streamlit_ace import st_ace
from pathlib import Path

from utils.mentor import mentor_reply
from utils.progress import init_progress, update_mastery
from utils.sandbox import check_exercise
from utils.tts import speak

# Resolve lessons path relative to this file, so it works on Streamlit Cloud
APP_DIR = Path(__file__).parent
LESSONS_PATH = APP_DIR / "lessons" / "python_basics.json"
with open(LESSONS_PATH) as f:
    LESSONS = json.load(f)

TRACK_ORDER = ["py.variables", "py.functions"]
SKILL_TO_LESSON = {"py.variables": "py-vars-01", "py.functions": "py-func-01"}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_skill" not in st.session_state:
    st.session_state.current_skill = TRACK_ORDER[0]

init_progress(TRACK_ORDER)

st.title(" Codespace Mentor ")

with st.sidebar:
    st.header("Progress")
    for sid in TRACK_ORDER:
        st.write(sid)
        st.progress(st.session_state.mastery[sid])

lesson_id = SKILL_TO_LESSON[st.session_state.current_skill]
lesson = LESSONS[lesson_id]

col_chat, col_lesson = st.columns([1, 1])

with col_chat:
    st.subheader("Mentor Chat")
    for role, msg in st.session_state.messages:
        st.chat_message(role).markdown(msg)

    user_text = st.chat_input("Ask the mentor...")
    if user_text:
        st.session_state.messages.append(("user", user_text))
        reply_text, voice_summary, actions = mentor_reply(user_text, lesson)
        st.session_state.messages.append(("assistant", reply_text))
        st.chat_message("assistant").markdown(reply_text)
        speak(voice_summary)

with col_lesson:
    st.subheader(f"Lesson: {lesson['title']}")
    st.write(lesson["overview"])
    st.code(lesson["example"], language="python")

    for ex in lesson["exercises"]:
        st.markdown(f"**{ex['prompt']}**")
        code_key = f"{lesson_id}:{ex['id']}"
        user_code = st_ace(language="python", key=code_key, height=140)
        if st.button(f"Run {ex['id']}", key=f"btn-{code_key}"):
            passed, feedback = check_exercise(ex, user_code or "")
            if passed:
                st.success(feedback)
                update_mastery(lesson["skill_id"], True)
                speak("Great job!")
            else:
                st.error(feedback)
                update_mastery(lesson["skill_id"], False)
                speak("Try again.")
