import streamlit as st
from core.smanager import StateManager

# Initialize triggers the rerun if LocalStorage data is found
StateManager.initialize()

st.set_page_config(page_title="AI Resume Generator", layout="wide", initial_sidebar_state="collapsed")

st.title("🚀 AI Powered Resume Generator")
st.write("Transform your experience into a recruiter-ready resume in minutes.")
st.divider()

try:
    resume_index = st.session_state.visited.index(False)
except ValueError:
    resume_index = len(StateManager.STEPS) - 1

left_col, spacer, right_col = st.columns([1, 3, 1])

with left_col:
    if st.button("Reset Session", icon=":material/restart_alt:"):
        # Clear both Session and LocalStorage
        st.session_state.form_data = {}
        st.session_state.visited = [False] * len(StateManager.STEPS)

        if StateManager.ls:
            StateManager.ls.deleteAll()
        
        st.rerun()

with right_col:
    # Button dynamically updates based on storage
    has_progress = any(st.session_state.visited)
    btn_label = "Continue" if has_progress else "Start"
    
    if st.button(btn_label, icon=":material/arrow_forward:"):
        st.switch_page(StateManager.get_page_path(resume_index))

if any(st.session_state.visited):
    st.info(f"💡 Progress detected! Resuming at Step {resume_index + 1}: **{StateManager.STEPS[resume_index]}**")