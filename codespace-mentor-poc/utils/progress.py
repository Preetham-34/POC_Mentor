import streamlit as st

def init_progress(track_order: list[str]):
    if "mastery" not in st.session_state:
        st.session_state.mastery = {k: 0.0 for k in track_order}

def update_mastery(skill_id: str, passed: bool):
    cur = st.session_state.mastery.get(skill_id, 0.0)
    delta = 0.15 if passed else -0.05
    st.session_state.mastery[skill_id] = float(max(0.0, min(1.0, cur + delta)))
